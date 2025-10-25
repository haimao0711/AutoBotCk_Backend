from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    
    def ready(self) -> None:
        logger.info('Stock App - Celery Beat scheduler enabled')
        logger.info('Stock download jobs are now managed by Celery Beat')
        logger.info('Make sure to run: celery -A config beat -l info')
        logger.info('And: celery -A config worker -l info')
        
        # APScheduler đã được thay thế bằng Celery Beat
        # Các scheduled tasks được định nghĩa trong apps/stock/scheduler/celery_scheduler.py
