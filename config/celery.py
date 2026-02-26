import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# 🔥 Force broker + backend (no fallback to AMQP)
app.conf.broker_url = os.getenv(
    "CELERY_BROKER_URL",
    "redis://redis:6379/0"
)

app.conf.result_backend = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://redis:6379/0"
)

# Load other CELERY_ settings
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")