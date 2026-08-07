from flask import Flask,request,jsonify
from flask_cors import CORS
from database import db,User,Student,Company
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