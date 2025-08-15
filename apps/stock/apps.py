from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    
    def ready(self) -> None:
        logger.info('Stock Download Job')
        from .scheduler import stock_imported as download_stock_job
        download_stock_job.start()
