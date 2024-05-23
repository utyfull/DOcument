from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DOcument.settings')

app = Celery('DOcument')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
