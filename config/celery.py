# import os
# from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# app = Celery("config")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()


# config/celery.py

import os
from celery import Celery

# This line is extremely important — it tells Celery to use your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app instance (name should match your project folder name)
app = Celery('config')

# Load ALL settings that start with CELERY_ from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically find @shared_task decorated functions in all apps
app.autodiscover_tasks()


# Optional: nice debug task
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')