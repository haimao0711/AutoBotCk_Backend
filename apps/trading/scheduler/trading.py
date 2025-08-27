from ..views import TradingViews
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging
import time
from django.db import connection, OperationalError
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.db import InterfaceError
logger = logging.getLogger(__name__)

# Quản lý Scheduler riêng cho từng user
user_schedulers = {}

def safe_run(func, user, job_name=""):
    try:
        # Đóng connection cũ trước khi chạy
        close_old_connections()

        func(user)

    except InterfaceError as e:
        logger.exception(f"❌ DB connection error trong job '{job_name}' của user {user.username}: {str(e)}")
        # Đóng connection lỗi, lần sau job sẽ dùng connection mới
        close_old_connections()

    except Exception as e:
        logger.exception(f"❌ Lỗi trong job '{job_name}' của user {user.username}: {str(e)}")

    finally:
        # Đảm bảo luôn đóng connection sau job
        close_old_connections()


def start_scheduler_for_user(user):
    """Bật Scheduler cho một user cụ thể, nếu bị crash thì tự động restart"""
    global user_schedulers

    if user.id in user_schedulers:
        scheduler = user_schedulers[user.id]
        if scheduler.running:
            logger.info(f"⚠️ Scheduler của user {user.username} đã chạy! Không cần restart.")
            return
        else:
            logger.warning(f"⚠️ Scheduler của user {user.username} đã bị dừng! Đang khởi động lại...")

    logger.info(f"🚀 Khởi động Scheduler cho user {user.username}...")

    scheduler = BackgroundScheduler(
        timezone='Asia/Ho_Chi_Minh',
        executors={'default': ThreadPoolExecutor(20)}
    )

    trading = TradingViews()

    scheduler.add_job(
        lambda: safe_run(trading.user_trading, user, "user_trading"),
        trigger=CronTrigger(day_of_week='mon-fri', hour='9-14', minute='*/1', timezone='Asia/Ho_Chi_Minh'),
        id=f"trade_{user.username}",
        replace_existing=True,
        max_instances=20
    )

    scheduler.add_job(
        lambda: safe_run(trading.cancel_trading, user, "cancel_trading_morning"),
        trigger=CronTrigger(day_of_week='mon-fri', hour=11, minute=29, timezone='Asia/Ho_Chi_Minh'),
        id=f"cancel_morning{user.username}",
        replace_existing=True,
        max_instances=1
    )

    scheduler.add_job(
        lambda: safe_run(trading.cancel_trading, user, "cancel_trading_afternoon"),
        trigger=CronTrigger(day_of_week='mon-fri', hour=14, minute=29, timezone='Asia/Ho_Chi_Minh'),
        id=f"cancel_afternoon{user.username}",
        replace_existing=True,
        max_instances=1
    )

    scheduler.add_job(
        lambda: safe_run(trading.restart_request_trade, user, "restart_request_trade"),
        trigger=CronTrigger(day_of_week='mon-fri', hour=14, minute=30, timezone='Asia/Ho_Chi_Minh'),
        id=f"restart_request_{user.username}",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
    print("Scheduler started for user:", user.username)
    user_schedulers[user.id] = scheduler  # dùng user.id thay vì object làm key
    print(f'check user_schedulers {user.username}: ', user_schedulers)
    # Chạy 1 lần ngay lập tức (cũng dùng safe_run)
    safe_run(trading.cancel_trading, user, "cancel_trading (initial)")
    safe_run(trading.restart_request_trade, user, "restart_request_trade (initial)")

    user.scheduler_status = True
    user.save()

    logger.info(f"✅ Scheduler đã khởi động thành công cho user {user.username}!")


def stop_scheduler_for_user(user):
    user_id = user.id
    if user_id in user_schedulers:
        scheduler = user_schedulers[user_id]
        scheduler.shutdown(wait=False)
        del user_schedulers[user_id]
        user.scheduler_status = False
        user.save()
        logger.info(f"⏹️ Scheduler đã dừng cho user {user.username} (id={user_id})")
    else:
        logger.warning(
            f"⚠️ Không tìm thấy Scheduler của user {user.username} (id={user_id}). "
            f"Hiện có: {list(user_schedulers.keys())}"
        )

def get_scheduler_status_for_user(user):
    """Lấy trạng thái Scheduler của user"""
    return {
        "user": user.username,
        "running": user.id in user_schedulers and user_schedulers[user.id].running
    }

def ensure_db_connection():
    """Tự động kết nối lại database nếu bị mất kết nối"""
    while True:
        try:
            connection.ensure_connection()
            logger.info("✅ Database kết nối thành công!")
            return
        except OperationalError:
            logger.warning("🔴 Database mất kết nối! Chờ 5 phút thử lại...")
            time.sleep(300)  # Đợi 5 phút rồi thử lại



def restart_schedulers():
    print('bắt đầu chạy hàm restart_schedulers')
    """Khi Django reload, kiểm tra user nào có scheduler_status = True thì chạy lại Scheduler"""
    ensure_db_connection()  # Đảm bảo database kết nối trước khi truy vấn

    User = get_user_model()
    users_with_scheduler = User.objects.filter(scheduler_status=True)
    if not users_with_scheduler.exists():
        logger.info("🔄 Không có user nào có Scheduler đang chạy.")
        return

    logger.info(f"🔄 Restarting Scheduler cho {users_with_scheduler.count()} user(s)...")

    for user in users_with_scheduler:
        try:
            start_scheduler_for_user(user)
        except Exception as e:
            logger.exception(f"❌ Lỗi khi restart Scheduler cho user {user.username}: {e}")

    logger.info("✅ Hoàn thành việc restart Scheduler cho các user.")


def check_scheduler_health():
    from apps.authencation.user.models import User  # Điều chỉnh import nếu cần
    logger.info("🔍 Kiểm tra trạng thái các scheduler...")

    for user_id, scheduler in list(user_schedulers.items()):
        try:
            # Chỉ restart nếu scheduler chết và user vẫn có flag scheduler_status=True
            user = User.objects.get(id=user_id)
            print(f'check {user.username} user_schedulers check_scheduler_health : ', user_id)
            print(f'check {user.username} scheduler.running check_scheduler_health : ', scheduler.running)
            print(f'check {user.username} user.scheduler_status check_scheduler_health : ', user.scheduler_status)
            if not scheduler.running and user.scheduler_status:
                print(f"⚠️ Scheduler của user {user.username} đã tắt. Đang khởi động lại.")
                logger.warning(f"⚠️ Scheduler của user {user.username} đã tắt. Đang khởi động lại.")
                start_scheduler_for_user(user)
        except User.DoesNotExist:
            print(f"⚠️ Không tìm thấy user với ID {user_id}. Xóa scheduler khỏi bộ nhớ.")
            logger.warning(f"⚠️ Không tìm thấy user với ID {user_id}. Xóa scheduler khỏi bộ nhớ.")
            del user_schedulers[user_id]
        except Exception as e:
            print(f"❌ Lỗi khi kiểm tra scheduler user ID {user_id}: {e}")
            logger.exception(f"❌ Lỗi khi kiểm tra scheduler user ID {user_id}: {e}")


