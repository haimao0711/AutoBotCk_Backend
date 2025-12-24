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

# Fix ReadOnlyError: Disable restoring unacked messages to prevent write operations
# on Redis during worker startup
try:
    from kombu.transport.redis import QoS
    
    # Override restore_visible to do nothing
    original_restore_visible = QoS.restore_visible
    
    def noop_restore_visible(self, num=0):
        """Disable restoring unacked messages to avoid ReadOnlyError"""
        return []
    
    # Patch the method
    QoS.restore_visible = noop_restore_visible
except (ImportError, AttributeError):
    pass  # kombu not available or method doesn't exist, skip patching

# Note: Both Stock and Trading schedulers use DatabaseScheduler (django_celery_beat)
# Schedules are stored in database and created via:
# - Stock: apps.stock.scheduler.celery_scheduler.setup_stock_schedules()
# - Trading: apps.trading.scheduler.celery_scheduler.create_user_schedules(user)
#
# To initialize schedules, run Django management command or call setup functions manually

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
