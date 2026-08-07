from celery_worker import celery_app
from flask import render_template
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from database import db, User, Student, Company, Job, Application

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='pc@gmail.com'
SENDER_PASSWORD=''

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    # s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def daily_reminder():
    users = User.query.all()
    for user in users:
        if user.role == "student":
            student = Student.query.filter_by(user_id=user.id).first()
            if student:
                message = f"Hello {user.name},\n\nThis is your daily reminder to check the latest job postings and updates on our platform. Don't miss out on any opportunities!\n\nBest regards,\nPlacement Portal Team"
                send_email(user.email, "Daily Reminder", message)
    return "Daily reminder emails sent successfully."

@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role="admin").first()
    
    # Put EVERYTHING inside this block!
    if admin:
        users_list = User.query.all()
        
        # Notice we use users=users_list to match {% for user in users %}
        html_report = render_template('monthly_report.html', users=users_list)
        
        send_email(admin.email, "Monthly User Report", html_report, content="html")
