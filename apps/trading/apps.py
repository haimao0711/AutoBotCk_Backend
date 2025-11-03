from django.apps import AppConfig
import logging
import os
import sys

logger = logging.getLogger(__name__)

class TradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.trading'

    def ready(self) -> None:
        # Kiểm tra xem có đang chạy flower command không
        # Flower không cần database, chỉ cần Redis để monitor Celery
        is_flower = 'flower' in ' '.join(sys.argv).lower()
        
        # Kiểm tra xem có POSTGRES_HOST environment variable không
        # Nếu không có, có thể là flower hoặc service không cần database
        has_postgres_config = os.getenv('POSTGRES_HOST')
        
        if is_flower or not has_postgres_config:
            if is_flower:
                logger.info('🌸 Bỏ qua bootstrap database cho Celery Flower (không cần DB)')
            else:
                logger.info('⚠️  Bỏ qua bootstrap database (không có POSTGRES_HOST config)')
            return
        
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