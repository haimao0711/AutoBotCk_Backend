import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from ..views import StockImportedViews
from django.db import close_old_connections  # ✅ thêm import

logger = logging.getLogger(__name__)
scheduler = None
scheduler_started = False

def safe_run(func):
    try:
        close_old_connections()  # ✅ Đóng connection cũ trước khi job chạy
        func()
    except Exception as e:
        logger.exception(f"Error running scheduled job: {e}")

def start():
    global scheduler, scheduler_started
    if scheduler_started:
        logger.info("Scheduler is already initialized.")
        return

    scheduler = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')

    stock_imported = StockImportedViews()

    triggers = {
        'trigger_w1': CronTrigger(day_of_week='mon', hour='9', minute='0', timezone='Asia/Ho_Chi_Minh'),
        'trigger_d1': CronTrigger(hour='9', minute='0', timezone='Asia/Ho_Chi_Minh'),
        'trigger_h1': CronTrigger(minute='0', timezone='Asia/Ho_Chi_Minh'),
        'trigger_m15': CronTrigger(minute='0,15,30,45', timezone='Asia/Ho_Chi_Minh'),
        'trigger_m5': CronTrigger(minute='0,5,10,15,20,25,30,35,40,45,50,55', timezone='Asia/Ho_Chi_Minh'),
        'trigger_m1': CronTrigger(minute='*', timezone='Asia/Ho_Chi_Minh'),
    }

    scheduler.add_job(lambda: safe_run(stock_imported.delete_old_records), trigger=triggers['trigger_h1'], id="stock_data_delete_h1", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_w1), trigger=triggers['trigger_w1'], id="stock_data_download_w1", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_d1), trigger=triggers['trigger_d1'], id="stock_data_download_d1", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_h1), trigger=triggers['trigger_h1'], id="stock_data_download_h1", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_m15), trigger=triggers['trigger_m15'], id="stock_data_download_m15", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_m5), trigger=triggers['trigger_m5'], id="stock_data_download_m5", replace_existing=True)
    scheduler.add_job(lambda: safe_run(stock_imported.save_stock_data_m1), trigger=triggers['trigger_m1'], id="stock_data_download_m1", replace_existing=True)

    try:
        scheduler.start()
        scheduler_started = True
        logger.info("Scheduler started.")
    except Exception as e:
        logger.exception(f"Failed to start scheduler: {e}")
