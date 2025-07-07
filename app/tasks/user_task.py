from app.celery_app import celery_app
import time

@celery_app.task
def send_welcome_email(user_id: int):
    print(f"📧 Sending welcome email to user {user_id}")
    time.sleep(2)  # 느린 작업 흉내
    return f"Email sent to user {user_id}"
