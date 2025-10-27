from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Note: Both Stock and Trading schedulers use DatabaseScheduler (django_celery_beat)
# Schedules are stored in database and created via:
# - Stock: apps.stock.scheduler.celery_scheduler.setup_stock_schedules()
# - Trading: apps.trading.scheduler.celery_scheduler.create_user_schedules(user)
#
# To initialize schedules, run Django management command or call setup functions manually

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
