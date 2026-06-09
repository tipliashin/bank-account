from celery import Celery

# Создаём экземпляр Celery
# broker_url — адрес Redis, куда складываются задачи
celery_app = Celery(
    'bankapi',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',  # для хранения результатов (опционально)
)

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