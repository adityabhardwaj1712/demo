# config/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Load settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discover tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")