from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String(20),nullable=False)

    #company approval
    is_approved=db.Column(db.Boolean,default=False)
    #blacklisting users
    is_blacklisted = db.Column(db.Boolean, default=False)

    # One to One relationship.Without uselist parameter by default its assumed that its one to many relationship
    student=db.relationship('Student', uselist=False, back_populates='user') 
    company=db.relationship('Company', uselist=False, back_populates='user') 
    
    #Password Hashing
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password,password)


class Student(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sdept=db.Column(db.String(100))
    scgpa=db.Column(db.Float)
    sphone=db.Column(db.String)
    resume = db.Column(db.LargeBinary)
    passing_year=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)

    #one to one
    user = db.relationship('User', back_populates='student')
    #Many to Many
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan") 

class Company(db.Model):
    __tablename__='companies'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    cwebsite=db.Column(db.String(200),nullable=False)
    hrcontact=db.Column(db.String(10),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    #One to One
    user = db.relationship('User', back_populates='company')

#Drives or Jobs Table
class Job(db.Model):
    __tablename__='jobs'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    jtitle=db.Column(db.String(120),nullable=False)
    jdesc=db.Column(db.String(200),nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    location=db.Column(db.String,nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    skills=db.Column(db.String(200),nullable=False)
    allowed_branches=db.Column(db.String(200),nullable=False)
    cgpa_criteria=db.Column(db.Float,nullable=False)
    graduation_year=db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    cid=db.Column(db.Integer,db.ForeignKey("companies.id"))
    #Many to Many
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")
    company = db.relationship("Company", backref="jobs") 


class Application(db.Model):
    __tablename__ = "applications"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    application_date = db.Column(db.Date)
    status = db.Column(db.String(20),nullable=False)
    interview_date_time = db.Column(db.DateTime,nullable=True)
    interview_location_link = db.Column(db.String(200),nullable=True)

    jid=db.Column(db.Integer,db.ForeignKey("jobs.id"))
    sid=db.Column(db.Integer,db.ForeignKey("students.id"))

    student = db.relationship("Student", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

