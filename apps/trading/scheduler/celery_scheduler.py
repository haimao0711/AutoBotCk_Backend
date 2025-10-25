from celery import shared_task
from celery.schedules import crontab
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def create_user_schedules(user):
    """
    Tạo schedules cho một user cụ thể
    """
    try:
        logger.info(f"Creating schedules for user: {user.username} (ID: {user.id})")
        # 1. User Trading Task - mỗi phút từ 9h-23h
        # Xóa duplicate schedules của user hiện tại trước
        PeriodicTask.objects.filter(
            name=f'user_trading_{user.username}'
        ).delete()
        
        schedule_trading, created = CrontabSchedule.objects.get_or_create(
            minute='*',
            hour='9-14',
            day_of_week='1-5',  # Monday to Friday
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        task_trading, created = PeriodicTask.objects.get_or_create(
            name=f'user_trading_{user.username}',
            defaults={
                'crontab': schedule_trading,
                'task': 'apps.trading.tasks.user_trading_task',
                'args': json.dumps([user.id]),
                'enabled': True,
                'queue': 'trading_high_priority'
            }
        )
        
        # 2. Cancel Trading Morning - 11:29
        # Xóa duplicate schedules của user hiện tại trước
        PeriodicTask.objects.filter(
            name=f'cancel_morning_{user.username}'
        ).delete()
        
        schedule_cancel_morning, created = CrontabSchedule.objects.get_or_create(
            minute='29',
            hour='11',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        task_cancel_morning, created = PeriodicTask.objects.get_or_create(
            name=f'cancel_morning_{user.username}',
            defaults={
                'crontab': schedule_cancel_morning,
                'task': 'apps.trading.tasks.cancel_trading_task',
                'args': json.dumps([user.id, 'morning']),
                'enabled': True,
                'queue': 'trading'
            }
        )
        
        # 3. Cancel Trading Afternoon - 14:29
        schedule_cancel_afternoon, created = CrontabSchedule.objects.get_or_create(
            minute='29',
            hour='14',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        task_cancel_afternoon, created = PeriodicTask.objects.get_or_create(
            name=f'cancel_afternoon_{user.username}',
            defaults={
                'crontab': schedule_cancel_afternoon,
                'task': 'apps.trading.tasks.cancel_trading_task',
                'args': json.dumps([user.id, 'afternoon']),
                'enabled': True,
                'queue': 'trading'
            }
        )
        
        # 4. Restart Request Trade - 14:30
        schedule_restart, created = CrontabSchedule.objects.get_or_create(
            minute='30',
            hour='14',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        task_restart, created = PeriodicTask.objects.get_or_create(
            name=f'restart_request_{user.username}',
            defaults={
                'crontab': schedule_restart,
                'task': 'apps.trading.tasks.restart_request_trade_task',
                'args': json.dumps([user.id]),
                'enabled': True,
                'queue': 'trading'
            }
        )
        
        logger.info(f"✅ Đã tạo schedules cho user {user.username}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Lỗi tạo schedules cho user {user.username}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def remove_user_schedules(user):
    """
    Xóa schedules của một user
    """
    try:
        PeriodicTask.objects.filter(
            name__in=[
                f'user_trading_{user.username}',
                f'cancel_morning_{user.username}',
                f'cancel_afternoon_{user.username}',
                f'restart_request_{user.username}'
            ]
        ).delete()
        
        logger.info(f"✅ Đã xóa schedules cho user {user.username}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Lỗi xóa schedules cho user {user.username}: {e}")
        return False

def restart_all_user_schedules():
    """
    Restart schedules cho tất cả users có scheduler_status=True
    """
    try:
        users_with_scheduler = User.objects.filter(scheduler_status=True)
        
        if not users_with_scheduler.exists():
            logger.info("🔄 Không có user nào có Scheduler đang chạy.")
            return
            
        logger.info(f"🔄 Restarting Celery schedules cho {users_with_scheduler.count()} user(s)...")
        
        for user in users_with_scheduler:
            try:
                create_user_schedules(user)
            except Exception as e:
                logger.exception(f"❌ Lỗi khi restart schedules cho user {user.username}: {e}")
                
        logger.info("✅ Hoàn thành việc restart Celery schedules cho các user.")
        
    except Exception as e:
        logger.error(f"❌ Lỗi trong restart_all_user_schedules: {e}")

def get_user_schedule_status(user):
    """
    Lấy trạng thái schedules của user
    """
    try:
        tasks = PeriodicTask.objects.filter(
            name__in=[
                f'user_trading_{user.username}',
                f'cancel_morning_{user.username}',
                f'cancel_afternoon_{user.username}',
                f'restart_request_{user.username}'
            ]
        )
        
        enabled_tasks = tasks.filter(enabled=True).count()
        total_tasks = tasks.count()
        
        return {
            "user": user.username,
            "enabled_tasks": enabled_tasks,
            "total_tasks": total_tasks,
            "status": "active" if enabled_tasks > 0 else "inactive"
        }
        
    except Exception as e:
        logger.error(f"❌ Lỗi lấy trạng thái schedules cho user {user.username}: {e}")
        return {
            "user": user.username,
            "enabled_tasks": 0,
            "total_tasks": 0,
            "status": "error"
        }
