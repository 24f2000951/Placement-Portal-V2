from flask import Flask,request,jsonify,send_file
import io
from flask_cors import CORS
from database import db,User,Student,Company,Job,Company,Application
from datetime import datetime,timezone
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)

db.init_app(app)

CORS(app)

@app.route('/api/register', methods=['POST'])
def register():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    name=data.get('name')
    email=data.get('email')
    password=data.get('password')
    role=data.get('role').lower()

    if role=='recruiter':
        role='company'

    if not all([name,email,password,role]):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user=User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400

    company_profile=None

    user=User(
        name=name,email=email,
        role=role,
        is_approved=False if role == 'company' else True,
        is_blacklisted=False)
    
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    if role == 'company':
        website = data.get('website')
        hrcontact = data.get('hrcontact')
        
        if not website or not hrcontact:
            return jsonify({"error": "Website and HR Contact are required for company registration"}), 400

        company_profile = Company(
            cwebsite=website,
            hrcontact=hrcontact,
            user_id=user.id
        )

        db.session.add(company_profile)

    elif role == 'student':
        student_profile = Student(
            user_id=user.id,
            sdept="",         
            scgpa=0.0,
            sphone="",
            passing_year=0
        )
        db.session.add(student_profile)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    email=data.get('email')
    password=data.get('password')

    user=User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid credentials or user not found"}), 401

    if not user.check_password(password):
        return jsonify({"error": "Invalid credentials or user not found"}), 401

    if user.role == "company":
        if user.is_blacklisted:
            return jsonify({"error": "You have been blacklisted"}), 403
        if not user.is_approved:
            return jsonify({"error": "Please wait for approval"}), 403
        
    if user.role=="student":
        if user.is_blacklisted:
            return jsonify({"error": "You have been blacklisted"}), 403
        

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful", 
        "access_token": access_token, 
        "role": user.role
    }), 200
    

@app.route('/api/admin/companies',methods=['GET'])
@jwt_required()
def get_companies():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    company = User.query.filter_by(role="company").all()
    company_list = []
    for recruiter in company:
        company_profile = recruiter.company 
        if recruiter.is_approved:
            status = "Approved"
        elif recruiter.is_blacklisted:
            status = "Blacklisted"
        else:
            status = "Pending"

        company_list.append({
            "id": recruiter.id, 
            "name": recruiter.name, 
            "email": recruiter.email,
            "website": company_profile.cwebsite,
            "hrcontact": company_profile.hrcontact,
            "status": status,
        })
        
    return jsonify(company_list), 200

@app.route('/api/admin/companies/<int:company_id>/approve', methods=['POST'])
@jwt_required()
def approve_company(company_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    company = User.query.filter_by(id=company_id, role="company").first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    company.is_approved = True
    company.is_blacklisted = False
    db.session.commit()

    return jsonify({"message": "Company approved successfully"}), 200

@app.route('/api/admin/companies/<int:company_id>/reject', methods=['POST'])
@jwt_required()
def reject_company(company_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    company = User.query.filter_by(id=company_id, role="company").first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    company.is_blacklisted = True
    company.is_approved = False
    db.session.commit()
    return jsonify({"message": "Company rejected and blacklisted successfully"}), 200

@app.route('/api/admin/students',methods=['GET'])
@jwt_required()
def get_students():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    students = User.query.filter_by(role="student").all()
    student_list = []


    for student in students:
        if student.is_approved:
            status = "Approved"
        elif student.is_blacklisted:
            status = "Blacklisted"
        student_list.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "branch": student.student.sdept if student.student else "N/A",
            "phone":student.student.sphone if student.student else "N/A",
            "status":status,
        })
    return jsonify(student_list), 200


@app.route('/api/admin/students/<int:student_id>/approve', methods=['POST'])
@jwt_required()
def approve_student(student_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    student = User.query.filter_by(id=student_id, role="student").first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student.is_approved = True
    student.is_blacklisted = False
    db.session.commit()

    return jsonify({"message": "Student approved successfully"}), 200

@app.route('/api/admin/students/<int:student_id>/reject', methods=['POST'])
@jwt_required()
def reject_student(student_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    student = User.query.filter_by(id=student_id, role="student").first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student.is_blacklisted = True
    student.is_approved = False
    db.session.commit()
    return jsonify({"message": "Student rejected and blacklisted successfully"}), 200

@app.route('/api/company/profile', methods=['GET','PUT'])
@jwt_required()
def get_company_profile():
    current_user_id = int(get_jwt_identity())
    company = User.query.get(current_user_id)
    if not company or company.role != "company":
        return jsonify({"error": "Unauthorized access"}), 403

    if request.method=='GET':
        return jsonify({
            "id": company.id,
            "name": company.name,
            "email": company.email,
            "company": {
                "website": company.company.cwebsite,
                "hrcontact": company.company.hrcontact
            }
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400


        company.name = data.get('name', company.name)
        company.company.cwebsite = data.get('website', company.company.cwebsite)
        company.company.hrcontact = data.get('hrcontact', company.company.hrcontact)

        db.session.commit()

        return jsonify({"message": "Company profile updated successfully!"}), 200

@app.route('/api/company/create-drive', methods=['POST'])
@jwt_required()
def create_drive():
    current_user_id = int(get_jwt_identity())
    
    user_account = User.query.get(current_user_id)
    if not user_account or user_account.role != "company":
        return jsonify({"error": "Unauthorized access"}), 403

    company_profile = user_account.company
    if not company_profile:
        return jsonify({"error": "Company profile not found"}), 404

    data = request.get_json()
    deadline_date = datetime.strptime(data["deadline"], "%Y-%m-%d").date()

    drive = Job(
        jtitle=data["title"],
        jdesc=data["description"],
        cgpa_criteria=data["cgpa"],
        allowed_branches=data["branches"],
        skills=data["skills"],
        salary=data["salary"],
        deadline=deadline_date,
        location=data["location"],
        graduation_year=data["year"],
        cid=company_profile.id,
        status="pending"
    )
    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Drive created successfully"}), 201

@app.route('/api/admin/drives', methods=['GET'])
@jwt_required()
def get_admin_drives():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    drives = Job.query.all()
    drive_list = []
    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "title": drive.jtitle,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "company": drive.company.user.name if drive.company and drive.company.user else "N/A",
            "location": drive.location,
            "salary": drive.salary,
            "skills": drive.skills,
            "allowed_branches": drive.allowed_branches,
            "cgpa_criteria": drive.cgpa_criteria,
            "graduation_year": drive.graduation_year,
            "description": drive.jdesc,
            "status": drive.status,
        })
    return jsonify(drive_list), 200

@app.route('/api/admin/drives/<int:drive_id>/approve', methods=['POST'])
@jwt_required()
def approve_drive(drive_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    drive = Job.query.get(drive_id)
    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    drive.status = "approved"
    db.session.commit()

    return jsonify({"message": "Drive approved successfully"}), 200

@app.route('/api/admin/drives/<int:drive_id>/reject', methods=['POST'])
@jwt_required()
def reject_drive(drive_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    drive = Job.query.get(drive_id)
    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    drive.status = "rejected"
    db.session.commit()

    return jsonify({"message": "Drive rejected successfully"}), 200

@app.route('/api/company/drives', methods=['GET'])
@jwt_required()
def get_company_drives():
    current_user_id = int(get_jwt_identity())
    user_account = User.query.get(current_user_id)
    
    if not user_account or user_account.role != "company":
        return jsonify({"error": "Unauthorized access"}), 403

    company_profile = user_account.company
    if not company_profile:
        return jsonify({"error": "Company profile not found"}), 404

    drive_type = request.args.get('status', 'active').lower()

    if drive_type == 'active':
        jobs = Job.query.filter(
            Job.cid == company_profile.id,
            Job.status == "approved"
        ).all()
    elif drive_type in ['history', 'completed']:
        jobs = Job.query.filter(
            Job.cid == company_profile.id,
            Job.status.in_(["closed", "rejected"])
        ).all()
    elif drive_type == 'pending':
        jobs = Job.query.filter(
            Job.cid == company_profile.id,
            Job.status == "pending"
        ).all()
    else:
        jobs = []
    
    job_list = []
    for job in jobs:

        job_list.append({
            "id": job.id,
            "title": job.jtitle,
            "description": job.jdesc,              
            "cgpa_criteria": job.cgpa_criteria,             
            "allowed_branches": job.allowed_branches,      
            "skills": job.skills,                  
            "salary": job.salary,                  
            "location": job.location,              
            "graduation_year": job.graduation_year, 
            "applicant_count": len(job.applications),           
            "deadline": job.deadline.strftime("%Y-%m-%d") if job.deadline else "N/A",
            "posted_on": job.created_at.strftime("%Y-%m-%d") if hasattr(job, 'created_at') and job.created_at else "N/A",
            "status": job.status
        })

    
    return jsonify(job_list), 200

@app.route("/api/company/drives/<int:drive_id>", methods=["DELETE"])
def delete_job(drive_id):
    job = Job.query.get_or_404(drive_id)
    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job deleted successfully"}), 200

@app.route('/api/company/drives/<int:drive_id>/close', methods=['POST'])
@jwt_required()
def close_drive(drive_id):
    current_user_id = int(get_jwt_identity())
    user_account = User.query.get(current_user_id)
    
    if not user_account or user_account.role != "company":
        return jsonify({"error": "Unauthorized access"}), 403

    company_profile = user_account.company
    if not company_profile:
        return jsonify({"error": "Company profile not found"}), 404

    job = Job.query.filter_by(id=drive_id, cid=company_profile.id).first()
    if not job:
        return jsonify({"error": "Job not found"}), 404

    job.status = "closed"
    db.session.commit()

    return jsonify({"message": "Drive closed successfully"}), 200

@app.route('/api/student/profile', methods=['GET','PUT'])
@jwt_required()
def get_student_profile():
    current_user_id = int(get_jwt_identity())
    student = User.query.get(current_user_id)
    if not student or student.role != "student":
        return jsonify({"error": "Unauthorized access"}), 403

    if not student.student:
        return jsonify({"error": "Student profile details not found. Please complete your profile."}), 404

    if request.method=='GET':
        return jsonify({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "student": {
                        "dept": student.student.sdept,
                        "cgpa": student.student.scgpa,
                        "phone": student.student.sphone,
                        "passing_year": student.student.passing_year
                    }
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        student.name = data.get('name', student.name)
        student.student.sdept = data.get('dept', student.student.sdept)
        student.student.scgpa = data.get('cgpa', student.student.scgpa)
        student.student.sphone = data.get('phone', student.student.sphone)
        student.student.passing_year = data.get('passing_year', student.student.passing_year)

        db.session.commit()

        return jsonify({"message": "Profile updated successfully!"}), 200

@app.route('/api/student/drives', methods=['GET'])
@jwt_required()
def get_student_drives():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or user.role != "student":
        return jsonify({"error": "Unauthorized access"}), 403

    student_profile = user.student
    if not student_profile:
        return jsonify({"error": "Student profile not found"}), 404

    applied_drive_ids = [app.jid for app in student_profile.applications]

    drives = Job.query.filter_by(status="approved").all()
    drive_list = []
    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "title": drive.jtitle,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "company": drive.company.user.name if drive.company and drive.company.user else "N/A",
            "location": drive.location,
            "salary": drive.salary,
            "skills": drive.skills,
            "allowed_branches": drive.allowed_branches,
            "cgpa_criteria": drive.cgpa_criteria,
            "graduation_year": drive.graduation_year,
            "posted_on": drive.created_at.strftime("%Y-%m-%d") if hasattr(drive, 'created_at') and drive.created_at else "N/A",
            "description": drive.jdesc,
            "has_applied": drive.id in applied_drive_ids
        })
    return jsonify(drive_list), 200

@app.route('/api/student/drives/<int:drive_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_drive(drive_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user or user.role != "student":
        return jsonify({"error": "Unauthorized access"}), 403

    student_profile = user.student
    if not student_profile:
        return jsonify({"error": "Student profile not found"}), 404

    drive = Job.query.get(drive_id)
    if not drive:
        return jsonify({"error": "Drive not found"}), 404
    if student_profile.scgpa < drive.cgpa_criteria:
        return jsonify({"error": "You do not meet the CGPA criteria for this drive."}), 400
    if student_profile.sdept not in drive.allowed_branches.split(','):
        return jsonify({"error": "Your department is not eligible for this drive."}), 400
    if student_profile.passing_year != drive.graduation_year:
        return jsonify({"error": "Your graduation year does not match the drive's requirement."}), 400

    existing_application = Application.query.filter_by(sid=student_profile.id, jid=drive_id).first()
    if existing_application:
        return jsonify({"error": "You have already applied for this drive."}), 400

    new_application = Application(
        sid=student_profile.id,
        jid=drive_id,
        status="Applied",
        application_date=datetime.now(timezone.utc).date()
    )
    db.session.add(new_application)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully!"}), 200

@app.route('/api/student/applications', methods=['GET'])
@jwt_required()
def get_student_applications():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user or user.role != "student":
        return jsonify({"error": "Unauthorized access"}), 403

    student_profile = user.student
    if not student_profile:
        return jsonify({"error": "Student profile not found"}), 404

    applications = Application.query.filter_by(sid=student_profile.id).all()
    application_list = []
    for application in applications:
        drive = application.job
        if drive:
            company_name = "N/A"
            if drive.company and drive.company.user:
                company_name = drive.company.user.name
            
        application_list.append({
                "application_id": application.id,
                "drive_id": drive.id,
                "title": drive.jtitle,
                "company": company_name,
                "status": application.status,
                "application_date": application.application_date.strftime("%Y-%m-%d") if application.application_date else "N/A",
                "description": drive.jdesc,
                "location": drive.location,
                "salary": drive.salary,
                "skills": drive.skills,
                "allowed_branches": drive.allowed_branches,
                "cgpa_criteria": drive.cgpa_criteria,
                "graduation_year": drive.graduation_year,
                "deadline": drive.deadline.strftime("%Y-%m-%d") if drive.deadline else "N/A"
            })
    return jsonify(application_list), 200

@app.route('/api/company/drives/<int:drive_id>/applicants', methods=['GET'])
@jwt_required()
def get_drive_applicants(drive_id):
    current_user_id = int(get_jwt_identity())
    user_account = User.query.get(current_user_id)
    
    if not user_account or user_account.role != "company":
        return jsonify({"error": "Unauthorized access"}), 403

    company_profile = user_account.company
    if not company_profile:
        return jsonify({"error": "Company profile not found"}), 404

    drive = Job.query.filter_by(id=drive_id, cid=company_profile.id).first()
    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    applications = Application.query.filter_by(jid=drive_id).all()
    applicant_list = []
    for application in applications:
        student = application.student
        if student:
            applicant_list.append({
                "application_id": application.id,
                "student_id": student.id,
                "name": student.user.name,
                "email": student.user.email,
                "dept": student.sdept,
                "cgpa": student.scgpa,
                "phone": student.sphone,
                "passing_year": student.passing_year,
                "status": application.status,
                "application_date": application.application_date.strftime("%Y-%m-%d") if application.application_date else "N/A"
            })
    return jsonify(applicant_list), 200

@app.route('/api/admin/applicants', methods=['GET'])
@jwt_required()
def get_all_applicants():
    current_user_id = int(get_jwt_identity())
    user_account = User.query.get(current_user_id)
    
    if not user_account or user_account.role != "admin":
        return jsonify({"error": "Unauthorized access. Admins only."}), 403

    applications = Application.query.all()
    
    applicant_list = []
    
    for app in applications:
        student = app.student
        job = app.job
        company = job.company if job else None

        if not student or not job:
            continue

        applicant_list.append({
            "id": app.id,
            "student_id": student.id,
            "student_name": student.user.name if student.user else "N/A",
            "job_title": job.jtitle,
            "company_name": company.user.name if company else "Unknown",
            "applied_on": app.application_date.strftime("%Y-%m-%d") if hasattr(app, 'application_date') and app.application_date else "N/A",
            "status": app.status
        })

    return jsonify(applicant_list), 200

@app.route('/api/student/resume', methods=['GET', 'POST'])
@jwt_required()
def handle_resume():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    student = user.student

    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    if request.method == 'POST':
        file = request.files.get('resume')
        if not file or not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Please upload a valid PDF file."}), 400
        
        student.resume = file.read()  # Save binary data to DB
        db.session.commit()
        return jsonify({"message": "Resume uploaded successfully!"}), 200
    
    if request.method == 'GET':
        if not student.resume:
            return jsonify({"error": "No resume found."}), 404
        
        return send_file(
            io.BytesIO(student.resume),
            mimetype='application/pdf',
            as_attachment=True, # as_attachment=True makes it an easy download
            download_name=f"{user.name.replace(' ', '_')}_Resume.pdf"
        )


def create_admin():
    existing_admin = User.query.filter_by(email="admin@gmail.com").first()
    if not existing_admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            role="admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)