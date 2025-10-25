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

# Setup schedulers for different apps
def setup_all_schedulers():
    """Setup all Celery Beat schedulers"""
    try:
        # Setup stock scheduler
        from apps.stock.scheduler.celery_scheduler import setup_stock_celery_scheduler
        setup_stock_celery_scheduler(app)
    except ImportError as e:
        print(f"Could not import stock scheduler: {e}")
    
    try:
        # Setup trading scheduler if exists
        from apps.trading.scheduler.celery_scheduler import setup_trading_celery_scheduler
        setup_trading_celery_scheduler(app)
    except ImportError as e:
        print(f"Could not import trading scheduler: {e}")

# Setup schedulers when Celery app is ready
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    setup_all_schedulers()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
