from celery import Celery
from dotenv import load_dotenv
load_dotenv()
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

celery_app = Celery(
    'bankapi',
    broker=f'{REDIS_URL}/0',
    backend=f'{REDIS_URL}/1',
)
# Создаём экземпляр Celery
# broker_url — адрес Redis, куда складываются задачи
# celery_app = Celery(
#     'bankapi',
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/1',  # для хранения результатов (опционально)
# )

# Настройки (опционально)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

# Явный импорт задач, чтобы Celery их видел
import tasks  # noqa: F401