from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class StockSocketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stockSocket'

    def ready(self):
        from .services.socket_service import start_socket
        logger.info("Starting stock socket service...")
        start_socket()
