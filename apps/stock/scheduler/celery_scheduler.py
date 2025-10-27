from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging

logger = logging.getLogger(__name__)

def get_or_create_crontab(minute, hour, day_of_week='*', day_of_month='*', month_of_year='*', timezone='Asia/Ho_Chi_Minh'):
    """
    Tìm hoặc tạo CrontabSchedule, xử lý duplicate nếu có
    """
    schedules = CrontabSchedule.objects.filter(
        minute=str(minute),
        hour=str(hour),
        day_of_week=str(day_of_week),
        day_of_month=str(day_of_month),
        month_of_year=str(month_of_year),
        timezone=timezone
    )
    
    count = schedules.count()
    
    if count == 0:
        return CrontabSchedule.objects.create(
            minute=str(minute),
            hour=str(hour),
            day_of_week=str(day_of_week),
            day_of_month=str(day_of_month),
            month_of_year=str(month_of_year),
            timezone=timezone
        )
    elif count == 1:
        return schedules.first()
    else:
        logger.warning(f"⚠️  Phát hiện {count} duplicate CrontabSchedule, đang dọn dẹp...")
        schedules.delete()
        return CrontabSchedule.objects.create(
            minute=str(minute),
            hour=str(hour),
            day_of_week=str(day_of_week),
            day_of_month=str(day_of_month),
            month_of_year=str(month_of_year),
            timezone=timezone
        )

def create_or_update_periodic_task(name, crontab, task, args='[]', queue='default'):
    """
    Tạo hoặc cập nhật PeriodicTask, xử lý duplicate nếu có
    """
    tasks = PeriodicTask.objects.filter(name=name)
    count = tasks.count()
    
    if count == 0:
        return PeriodicTask.objects.create(
            name=name,
            crontab=crontab,
            task=task,
            args=args,
            enabled=True,
            queue=queue
        )
    elif count == 1:
        task_obj = tasks.first()
        task_obj.crontab = crontab
        task_obj.task = task
        task_obj.args = args
        task_obj.enabled = True
        task_obj.queue = queue
        task_obj.save()
        return task_obj
    else:
        logger.warning(f"⚠️  Phát hiện {count} duplicate PeriodicTask '{name}', đang dọn dẹp...")
        tasks.delete()
        return PeriodicTask.objects.create(
            name=name,
            crontab=crontab,
            task=task,
            args=args,
            enabled=True,
            queue=queue
        )

def setup_stock_schedules():
    """
    Tạo PeriodicTask trong database cho các task download stock data
    Thay thế cho APScheduler
    """
    try:
        logger.info("🔄 Creating Stock data download schedules in database...")
        
        # 1. Delete old records - Hàng giờ từ 9:00-15:00
        schedule_delete = get_or_create_crontab(
            minute='0',
            hour='9-15'
        )
        create_or_update_periodic_task(
            name='delete_old_stock_records',
            crontab=schedule_delete,
            task='apps.stock.tasks.delete_old_stock_records_task',
            queue='default'
        )
        
        # 2. Download W1 - Thứ 2 hàng tuần lúc 9:00
        schedule_w1 = get_or_create_crontab(
            minute='0',
            hour='9',
            day_of_week='1'
        )
        create_or_update_periodic_task(
            name='download_stock_data_w1',
            crontab=schedule_w1,
            task='apps.stock.tasks.download_stock_data_w1_task',
            queue='default'
        )
        
        # 3. Download D1 - Hàng ngày lúc 9:00
        schedule_d1 = get_or_create_crontab(
            minute='0',
            hour='9'
        )
        create_or_update_periodic_task(
            name='download_stock_data_d1',
            crontab=schedule_d1,
            task='apps.stock.tasks.download_stock_data_d1_task',
            queue='default'
        )
        
        # 4. Download H1 - Hàng giờ từ 9:00-15:00
        schedule_h1 = get_or_create_crontab(
            minute='0',
            hour='9-15'
        )
        create_or_update_periodic_task(
            name='download_stock_data_h1',
            crontab=schedule_h1,
            task='apps.stock.tasks.download_stock_data_h1_task',
            queue='default'
        )
        
        # 5. Download M15 - Mỗi 15 phút từ 9:00-15:00
        schedule_m15 = get_or_create_crontab(
            minute='0,15,30,45',
            hour='9-15'
        )
        create_or_update_periodic_task(
            name='download_stock_data_m15',
            crontab=schedule_m15,
            task='apps.stock.tasks.download_stock_data_m15_task',
            queue='default'
        )
        
        # 6. Download M5 - Mỗi 5 phút từ 9:00-15:00
        schedule_m5 = get_or_create_crontab(
            minute='0,5,10,15,20,25,30,35,40,45,50,55',
            hour='9-15'
        )
        create_or_update_periodic_task(
            name='download_stock_data_m5',
            crontab=schedule_m5,
            task='apps.stock.tasks.download_stock_data_m5_task',
            queue='default'
        )
        
        # 7. Download M1 - Mỗi phút từ 9:00-15:00
        schedule_m1 = get_or_create_crontab(
            minute='*',
            hour='9-15'
        )
        create_or_update_periodic_task(
            name='download_stock_data_m1',
            crontab=schedule_m1,
            task='apps.stock.tasks.download_stock_data_m1_task',
            queue='default'
        )
        
        logger.info("✅ Stock schedules created successfully!")
        logger.info("Scheduled tasks:")
        logger.info("  - delete_old_stock_records: Every hour from 9:00-15:00")
        logger.info("  - download_stock_data_w1: Every Monday at 9:00")
        logger.info("  - download_stock_data_d1: Every day at 9:00")
        logger.info("  - download_stock_data_h1: Every hour from 9:00-15:00")
        logger.info("  - download_stock_data_m15: Every 15 minutes from 9:00-15:00")
        logger.info("  - download_stock_data_m5: Every 5 minutes from 9:00-15:00")
        logger.info("  - download_stock_data_m1: Every minute from 9:00-15:00")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Lỗi tạo Stock schedules: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False
