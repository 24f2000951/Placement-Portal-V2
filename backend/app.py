from flask import Flask,request,jsonify
from database import db,User

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/')
def home():
    return "Hello"


def create_admin():
    existing_admin = User.query.filter_by(email="admin@mail.com").first()
    if not existing_admin:
        admin = User(
            name="Admin",
            email="admin@mail.com",
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