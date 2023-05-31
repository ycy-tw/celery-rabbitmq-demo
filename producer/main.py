from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue
from pydantic import BaseSettings


default_exchange = Exchange(name='default', type='direct')

class CelerySettings(BaseSettings):
    result_backend: str | None
    broker_url: str
    enable_utc: bool = False
    task_track_started: bool = True
    task_default_exchange: str = default_exchange.name
    task_default_exchange_type: str = default_exchange.type
    task_queues: list[Queue] | None
    beat_schedule: dict = {
        "send_email_to_customer": {
            "task": "tasks.send_email_to_customer",
            "schedule": crontab(minute='*/1'),
        },
    }

    class Config:
        env_file = ".env"
        env_prefix = "CELERY_"

settings = CelerySettings()
app = Celery(main='producer', include=['tasks'])
app.config_from_object(settings)