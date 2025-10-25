from celery import Celery
from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)

def setup_stock_celery_scheduler(app: Celery):
    """
    Thiết lập Celery Beat scheduler cho các task download stock data
    Thay thế cho APScheduler trong stock_imported.py
    """
    
    # Import các tasks
    from apps.stock.tasks import (
        download_stock_data_w1_task,
        download_stock_data_d1_task,
        download_stock_data_h1_task,
        download_stock_data_m15_task,
        download_stock_data_m5_task,
        download_stock_data_m1_task,
        delete_old_stock_records_task
    )
    
    # Cấu hình timezone
    app.conf.timezone = 'Asia/Ho_Chi_Minh'
    
    # Định nghĩa các periodic tasks
    app.conf.beat_schedule = {
        # Xóa dữ liệu cũ - chạy hàng giờ từ 9:00-15:00
        'delete-old-stock-records': {
            'task': 'apps.stock.tasks.delete_old_stock_records_task',
            'schedule': crontab(hour='9-15', minute=0, timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download W1 - chạy thứ 2 hàng tuần lúc 9:00
        'download-stock-data-w1': {
            'task': 'apps.stock.tasks.download_stock_data_w1_task',
            'schedule': crontab(day_of_week=1, hour=9, minute=0, timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download D1 - chạy hàng ngày lúc 9:00
        'download-stock-data-d1': {
            'task': 'apps.stock.tasks.download_stock_data_d1_task',
            'schedule': crontab(hour=9, minute=0, timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download H1 - chạy hàng giờ từ 9:00-15:00
        'download-stock-data-h1': {
            'task': 'apps.stock.tasks.download_stock_data_h1_task',
            'schedule': crontab(hour='9-15', minute=0, timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download M15 - chạy mỗi 15 phút từ 9:00-15:00
        'download-stock-data-m15': {
            'task': 'apps.stock.tasks.download_stock_data_m15_task',
            'schedule': crontab(hour='9-15', minute='0,15,30,45', timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download M5 - chạy mỗi 5 phút từ 9:00-15:00
        'download-stock-data-m5': {
            'task': 'apps.stock.tasks.download_stock_data_m5_task',
            'schedule': crontab(hour='9-15', minute='0,5,10,15,20,25,30,35,40,45,50,55', timezone='Asia/Ho_Chi_Minh'),
        },
        
        # Download M1 - chạy mỗi phút từ 9:00-15:00
        'download-stock-data-m1': {
            'task': 'apps.stock.tasks.download_stock_data_m1_task',
            'schedule': crontab(hour='9-15', minute='*', timezone='Asia/Ho_Chi_Minh'),
        },
    }
    
    logger.info("Stock Celery Beat scheduler configured successfully")
    logger.info("Scheduled tasks:")
    logger.info("- delete-old-stock-records: Every hour from 9:00-15:00")
    logger.info("- download-stock-data-w1: Every Monday at 9:00")
    logger.info("- download-stock-data-d1: Every day at 9:00")
    logger.info("- download-stock-data-h1: Every hour from 9:00-15:00")
    logger.info("- download-stock-data-m15: Every 15 minutes from 9:00-15:00")
    logger.info("- download-stock-data-m5: Every 5 minutes from 9:00-15:00")
    logger.info("- download-stock-data-m1: Every minute from 9:00-15:00")
