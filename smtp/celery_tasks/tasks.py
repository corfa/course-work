from celery import Celery

from SMTP.server import send_email_verification
from celery_tasks.config_Celery import CeleryConfig

app = Celery(CeleryConfig.name, broker=CeleryConfig.url_broker)


@app.task
def task_email(recipient: str, token: str):
    send_email_verification(recipient, token)
    return "ok, message send"
