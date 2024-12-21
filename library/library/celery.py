from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

app = Celery('library')

# Configure Celery to use settings from Django's settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in registered Django apps
app.autodiscover_tasks()
