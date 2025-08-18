from django.apps import AppConfig
import logging
import os
import threading
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

class TradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.trading'

    def ready(self) -> None:
        if os.environ.get('RUN_MAIN') != 'true' and 'gunicorn' not in sys.argv:
         return

        logger.info('🚀 Bắt đầu khởi động hệ thống Scheduler và kiểm tra DB...')

        def bootstrap_schedulers():
            try:
                from .scheduler.trading import (
                    ensure_db_connection,
                    restart_schedulers,
                    check_scheduler_health,
                )
                from django.db import connection

                connection.ensure_connection()

                # Restart scheduler các user có flag True
                restart_schedulers()

                health_checker = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')
                health_checker.add_job(
                    check_scheduler_health,
                    trigger=CronTrigger(minute='*/3', hour='9-22'),  # Mỗi 15 phút trong giờ giao dịch
                    id="check_all_schedulers",
                    replace_existing=True
                )
                health_checker.add_job(
                    restart_schedulers,
                    trigger=CronTrigger(hour=8, minute=59),
                    id="daily_restart_schedulers",
                    replace_existing=True
                )
                health_checker.start()

                # Khởi động thread đảm bảo DB kết nối (nếu cần)
                threading.Thread(target=ensure_db_connection, daemon=True).start()

                logger.info("✅ Scheduler và Health Checker đã được khởi động!")
            except Exception as e:
                logger.exception(f"❌ Lỗi khởi động Scheduler hoặc DB: {e}")

        threading.Thread(target=bootstrap_schedulers, daemon=True).start()