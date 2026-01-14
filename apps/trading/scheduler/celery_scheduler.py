from celery import shared_task
from celery.schedules import crontab
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def get_or_create_crontab(minute, hour, day_of_week, day_of_month, month_of_year, timezone):
    """
    Tìm hoặc tạo CrontabSchedule, xử lý duplicate nếu có
    """
    schedules = CrontabSchedule.objects.filter(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
        timezone=timezone
    )
    
    count = schedules.count()
    
    if count == 0:
        # Không có schedule, tạo mới
        return CrontabSchedule.objects.create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            timezone=timezone
        )
    elif count == 1:
        # Có 1 schedule, dùng luôn
        return schedules.first()
    else:
        # Có duplicate, xóa hết và tạo mới
        logger.warning(f"⚠️  Phát hiện {count} duplicate CrontabSchedule, đang dọn dẹp...")
        schedules.delete()
        return CrontabSchedule.objects.create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            timezone=timezone
        )

def create_or_update_periodic_task(name, crontab, task, args, queue):
    """
    Tạo hoặc cập nhật PeriodicTask, xử lý duplicate nếu có
    """
    tasks = PeriodicTask.objects.filter(name=name)
    count = tasks.count()
    
    if count == 0:
        # Không có task, tạo mới
        return PeriodicTask.objects.create(
            name=name,
            crontab=crontab,
            task=task,
            args=args,
            enabled=True,
            queue=queue
        )
    elif count == 1:
        # Có 1 task, update
        task_obj = tasks.first()
        task_obj.crontab = crontab
        task_obj.task = task
        task_obj.args = args
        task_obj.enabled = True
        task_obj.queue = queue
        task_obj.save()
        return task_obj
    else:
        # Có duplicate, xóa hết và tạo mới
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

def create_user_schedules(user):
    """
    Tạo schedules cho một user cụ thể
    """
    try:
        logger.info(f"Creating schedules for user: {user.username} (ID: {user.id})")
        
        # 1. User Trading Task - mỗi phút từ 9h-14h
        schedule_trading = get_or_create_crontab(
            minute='*',
            hour='9-23',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        create_or_update_periodic_task(
            name=f'user_trading_{user.username}',
            crontab=schedule_trading,
            task='apps.trading.tasks.user_trading_task',
            args=json.dumps([user.id]),
            queue='trading_high_priority'
        )
        
        # 2. Cancel Trading Morning - 11:29
        schedule_cancel_morning = get_or_create_crontab(
            minute='29',
            hour='11',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        create_or_update_periodic_task(
            name=f'cancel_morning_{user.username}',
            crontab=schedule_cancel_morning,
            task='apps.trading.tasks.cancel_trading_task',
            args=json.dumps([user.id, 'morning']),
            queue='trading'
        )
        
        # 3. Cancel Trading Afternoon - 14:29
        schedule_cancel_afternoon = get_or_create_crontab(
            minute='29',
            hour='14',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        create_or_update_periodic_task(
            name=f'cancel_afternoon_{user.username}',
            crontab=schedule_cancel_afternoon,
            task='apps.trading.tasks.cancel_trading_task',
            args=json.dumps([user.id, 'afternoon']),
            queue='trading'
        )
        
        # 4. Restart Request Trade - 14:30
        schedule_restart = get_or_create_crontab(
            minute='30',
            hour='14',
            day_of_week='1-5',
            day_of_month='*',
            month_of_year='*',
            timezone='Asia/Ho_Chi_Minh'
        )
        
        create_or_update_periodic_task(
            name=f'restart_request_{user.username}',
            crontab=schedule_restart,
            task='apps.trading.tasks.restart_request_trade_task',
            args=json.dumps([user.id]),
            queue='trading'
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

def cancel_all_orders_on_startup():
    """
    Hủy tất cả lệnh của tất cả users có scheduler_status=True khi container khởi động
    """
    try:
        from apps.account.detail.services import AccountService
        from apps.trading.service.handlers import cancel_all_orders
        from apps import api
        
        users_with_scheduler = User.objects.filter(scheduler_status=True)
        
        if not users_with_scheduler.exists():
            logger.info("🔄 Không có user nào có Scheduler đang chạy, không cần hủy lệnh.")
            return
            
        logger.info(f"🔄 Bắt đầu hủy tất cả lệnh cho {users_with_scheduler.count()} user(s) khi khởi động container...")
        
        for user in users_with_scheduler:
            try:
                vps_account = AccountService.get_account_by_user(user)
                if not vps_account:
                    logger.warning(f"⚠️ User {user.username} không có account, bỏ qua.")
                    continue
                    
                account_name = vps_account.name
                account_num = vps_account.account_num
                session_id = vps_account.vps_session_id
                url = api.TRADING_URL
                
                logger.info(f"🔄 Đang hủy tất cả lệnh cho user {user.username}...")
                cancel_all_orders(user, account_name, account_num, '', url, session_id, '', 'All')
                logger.info(f"✅ Đã hủy tất cả lệnh cho user {user.username}")
                
            except Exception as e:
                logger.exception(f"❌ Lỗi khi hủy lệnh cho user {user.username}: {e}")
                
        logger.info("✅ Hoàn thành việc hủy tất cả lệnh khi khởi động container.")
        
        
    except Exception as e:
        logger.exception(f"❌ Lỗi trong cancel_all_orders_on_startup: {e}")

def revert_all_trading_status_on_startup():
    """
    Revert trạng thái request trade (is_buy_hand, is_sell_hand) và is_trading về False 
    cho tất cả users khi container khởi động
    """
    try:
        from apps.configuration.details.overview.services import ConfigurationOverviewServices
        
        users = User.objects.all()
        
        if not users.exists():
            logger.info("🔄 Không có user nào trong hệ thống để revert status.")
            return
            
        logger.info(f"🔄 Bắt đầu revert trading status cho {users.count()} user(s) khi khởi động container...")
        
        for user in users:
            try:
                # Hàm này đã bao gồm logic update cả request trade (overview) và is_trading (trading config)
                ConfigurationOverviewServices.restart_request_trade_overview(user)
                
            except Exception as e:
                logger.exception(f"❌ Lỗi khi revert trading status cho user {user.username}: {e}")
                
        logger.info("✅ Hoàn thành việc revert trading status khi khởi động container.")
        
    except Exception as e:
        logger.exception(f"❌ Lỗi trong revert_all_trading_status_on_startup: {e}")
