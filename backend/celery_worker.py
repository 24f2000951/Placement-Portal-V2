from celery import Celery, Task
from celery.schedules import crontab
from app import app

celery_app = Celery('tasks',broker='redis://localhost:6379/1', backend='redis://localhost:6379/2',include=['tasks'])

class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
celery_app.Task = FlaskTask  

celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    # 'monthly_user_report': {
    #     'task': 'tasks.send_monthly_report',
    #     'schedule': 20.0,
    # },
    # 'daily_remainder':{
    #     'task': 'tasks.daily_reminder',
    #     'schedule': crontab(hour=23, minute=30),
    # },
    # 'interview_reminder':{
    #     'task': 'tasks.send_interview_reminder',
    #     'schedule': crontab(hour=20, minute=7),
    # },
    # 'generate_application_csv': {
    #     'task': 'tasks.generate_application_csv',
    #     'schedule': crontab(hour=23, minute=59),
    # }
}

                         
                                 