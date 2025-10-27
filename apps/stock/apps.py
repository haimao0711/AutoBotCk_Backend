from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    
    def ready(self) -> None:
        """
        Stock App - Celery Beat Scheduler enabled
        
        APScheduler đã được thay thế bằng Celery Beat + DatabaseScheduler.
        
        Để setup schedules, chạy:
            python manage.py setup_stock_schedules
        
        Hoặc gọi API endpoint:
            POST /api/stock/setup-schedules/
        """
        logger.info('Stock App loaded - Celery Beat scheduler ready')
