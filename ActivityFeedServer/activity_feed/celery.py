import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activity_feed.settings")

# Create the Celery application instance
app = Celery("activity_feed")

# Load the Celery configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in Django apps
app.autodiscover_tasks()
