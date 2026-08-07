from celery_worker import celery_app
from flask import render_template
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
import csv
import os
from database import  User, Student, Company, Job, Application

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
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def daily_reminder():
    registered_students = User.query.join(Student, User.id == Student.user_id)\
                                    .filter(User.role == "student").all()
    
    for user in registered_students:
        message = (
            f"Hello {user.name},\n\n"
            f"This is your daily reminder to check the latest job postings and updates on our platform. "
            f"Don't miss out on any opportunities!\n\n"
            f"Best regards,\n"
            f"Placement Portal Team"
        )
        send_email(user.email, "Daily Reminder", message)
        
    return f"Daily reminder emails sent successfully to {len(registered_students)} students."

@celery_app.task
def generate_application_csv():
    applications = Application.query.all()
    csv_filename = 'applications.csv'
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Application ID', 'Company Name', 'Job Title', 'Status','Application Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for application in applications:
            job = Job.query.get(application.jid)
            company = Company.query.get(job.cid) if job else None
            
            company_name = company.user.name if company and company.user else 'N/A'
            job_title = job.jtitle if job else 'N/A'
            
            writer.writerow({
                'Application ID': application.id,
                'Company Name': company_name,
                'Job Title': job_title,
                'Status': application.status,
                'Application Date': application.application_date
            })
    send_email(application.student.user.email, "Application CSV Report", "Report generated successfully.")
    
    return os.path.abspath(csv_filename)


    
@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role="admin").first()
    
    if admin:
        drives= Job.query.filter(Job.status != "rejected").all()
        drives_count = len(drives)

        applications = Application.query.all()

        unique_applied_sids = {app.sid for app in applications}
        students_applied_count = len(unique_applied_sids)

        unique_placed_sids = {app.sid for app in applications if app.status == "placed"}
        students_placed_count = len(unique_placed_sids)

       

        html_report = render_template('monthly_report.html',drives=drives,drives_count=drives_count,students_applied_count=students_applied_count,students_placed_count=students_placed_count)
        
        send_email(admin.email, "Monthly User Report", html_report, content="html")
