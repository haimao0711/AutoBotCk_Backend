from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class TradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.trading'

    def ready(self) -> None:
        logger.info('🚀 Bắt đầu khởi động hệ thống Celery và kiểm tra DB...')

        def bootstrap_celery_schedules():
            try:
                from django.db import connection
                from .scheduler.celery_scheduler import restart_all_user_schedules
                
                # Đảm bảo database kết nối
                connection.ensure_connection()
                
                # Restart schedules cho các user có flag True
                restart_all_user_schedules()
                
                logger.info("✅ Celery schedules đã được khởi động!")
                
            except Exception as e:
                logger.exception(f"❌ Lỗi khởi động Celery schedules hoặc DB: {e}")

        bootstrap_celery_schedules()