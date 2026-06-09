import time
from celery_app import celery_app

@celery_app.task
def send_welcome_email(user_name: str, user_email: str):
    """Имитация отправки письма."""
    print(f"Начинаем отправку письма для {user_name} ({user_email})...")
    time.sleep(5)  # имитация долгой работы
    print(f"Письмо для {user_name} успешно отправлено!")
    return f"Email sent to {user_email}"