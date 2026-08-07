from flask import Flask,request,jsonify
from flask_cors import CORS
from database import db,User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)

db.init_app(app)

CORS(app)  # Enable CORS for all routes

@app.route('/register', methods=['POST'])
def register():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    name=data.get('name')
    email=data.get('email')
    password=data.get('password')
    role=data.get('role')

    if not all([name,email,password,role]):
        return jsonify({"error": "Missing required fields"}), 400
    
    user=User(name=name,email=email,role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    email=data.get('email')
    password=data.get('password')
    role=data.get('role')

    user=User.query.filter_by(email=email,role=role).first()
    if user and user.check_password(password):
        access_token=create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token, "role": user.role}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

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