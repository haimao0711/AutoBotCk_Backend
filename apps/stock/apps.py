from django.apps import AppConfig
import logging
import os

logger = logging.getLogger(__name__)

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    
    def ready(self) -> None:
        # Chỉ chạy setup schedules trong Celery Beat process hoặc khi migrate
        # Tránh chạy trong worker hoặc web server
        import sys
        
        # Kiểm tra nếu đang chạy celery beat
        is_celery_beat = 'celery' in sys.argv and 'beat' in sys.argv
        
        # Hoặc chạy trong Django shell/management command
        is_management_command = len(sys.argv) > 1 and sys.argv[1] in ['shell', 'shell_plus', 'setup_stock_schedules']
        
        if is_celery_beat or is_management_command:
            try:
                # Import ở đây để tránh circular import
                from apps.stock.scheduler.celery_scheduler import setup_stock_schedules
                
                # Delay việc setup một chút để đảm bảo DB đã sẵn sàng
                from threading import Timer
                def delayed_setup():
                    try:
                        setup_stock_schedules()
                    except Exception as e:
                        logger.error(f"Failed to setup stock schedules: {e}")
                
                Timer(5.0, delayed_setup).start()
                logger.info('📅 Stock schedules will be initialized in 5 seconds...')
                
            except Exception as e:
                logger.error(f"Error initializing stock scheduler: {e}")
        else:
            logger.info('Stock App loaded (scheduler initialization skipped for this process)')
        
        # APScheduler đã được thay thế bằng Celery Beat + DatabaseScheduler
        # Các scheduled tasks được tạo trong database bởi setup_stock_schedules()
