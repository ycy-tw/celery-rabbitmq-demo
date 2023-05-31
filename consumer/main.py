from celery import Celery
from kombu import Exchange, Queue
from pydantic import BaseSettings


default_exchange = Exchange(name='default', type='direct')
email_queue = Queue(
    name='email',
    routing_key='notification.email.send', 
    exchange=default_exchange,
)
queues = [email_queue]

class CelerySettings(BaseSettings):
    result_backend: str | None
    broker_url: str
    enable_utc: bool = False
    task_track_started: bool = True
    task_default_exchange: str = default_exchange.name
    task_default_exchange_type: str = default_exchange.type
    task_queues: list[Queue] | None = queues
    beat_schedule: dict | None

    class Config:
        env_file = ".env"
        env_prefix = "CELERY_"

settings = CelerySettings()
app = Celery(main='consumer', include=['tasks'])
app.config_from_object(settings)