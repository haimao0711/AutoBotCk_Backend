# 🚀 Hướng dẫn Migration từ APScheduler sang Celery/RQ

## 📋 Tổng quan

Tài liệu này hướng dẫn chi tiết việc migration hệ thống trading scheduler từ APScheduler sang Celery/RQ để giải quyết vấn đề quá tải RAM và cải thiện hiệu suất.

---

## 🎯 Mục tiêu Migration

- **Giảm RAM usage** từ 40,000+ threads xuống < 100 processes
- **Cải thiện reliability** với task persistence và retry mechanisms
- **Tăng scalability** với horizontal scaling
- **Better monitoring** và debugging capabilities

---

## 📦 1. Cài đặt Dependencies

### 1.1 Thêm vào requirements.txt

```txt
# Thay thế APScheduler
# APScheduler==3.10.4  # ❌ Xóa dòng này

# Thêm Celery và Redis
celery==5.3.4
redis==5.0.1
django-celery-beat==2.5.0
django-celery-results==2.5.1

# Hoặc nếu chọn RQ (nhẹ hơn)
# rq==1.15.1
# django-rq==2.8.1
```

### 1.2 Cài đặt Redis

```bash
# Docker Compose
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data

# Hoặc cài đặt local
sudo apt-get install redis-server
```

---

## ⚙️ 2. Cấu hình Django Settings

### 2.1 Thêm vào settings/base.py

```python
# Celery Configuration
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Celery Beat (cho periodic tasks)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Celery Settings
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
CELERY_ENABLE_UTC = True

# Task Settings
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_ROUTES = {
    'apps.trading.tasks.*': {'queue': 'trading'},
    'apps.trading.tasks.user_trading': {'queue': 'trading_high_priority'},
}

# Worker Settings
CELERY_WORKER_CONCURRENCY = 10  # Giảm từ 100 threads xuống 10 processes
CELERY_WORKER_MAX_TASKS_PER_CHILD = 50  # Restart worker sau 50 tasks
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Retry Settings
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_MAX_RETRIES = 3

# Monitoring
CELERY_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps ...
    'django_celery_beat',
    'django_celery_results',
    'apps.trading',  # Đảm bảo có trading app
]
```

### 2.2 Environment Variables (.env)

```env
# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Celery Configuration
CELERY_WORKER_CONCURRENCY=10
CELERY_TASK_DEFAULT_QUEUE=default
```

---

## 🔄 3. Tạo Celery App

### 3.1 Tạo file apps/trading/celery.py

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('trading')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

### 3.2 Cập nhật apps/trading/__init__.py

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

## 📝 4. Chuyển đổi Tasks

### 4.1 Tạo file apps/trading/tasks.py

```python
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from apps.account.detail.services import AccountService
from apps.trading.service.handlers import trading, cancel_all_orders
from apps.configuration.details.overview.services import ConfigurationOverviewServices
from apps import api
import pytz
from datetime import datetime, time
from apps.trading.helper import is_within_range_time
from common.api.smartone.handler import validate_session
from apps.telegram.sender import send_message_telegram
from apps.telegram.enum.enums import MessageTypeEnum
from common.errors.messages import ErrorMessages

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def user_trading_task(self, user_id):
    """
    Celery task thay thế cho TradingViews.user_trading
    """
    try:
        user = User.objects.get(id=user_id)
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(timezone).time()

        morning_start = time(9, 15)
        morning_end = time(11, 28)
        afternoon_start = time(13, 0)
        afternoon_end = time(23, 28)
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id
        
        logger.info(f'Đã chạy hàm user_trading của user {account_name} với tài khoản {account_num}')

        if is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end):
            url = api.TRADING_URL
            is_validate_session, res_validate_session = validate_session(account_name, account_num, url, session_id, '')
            
            if not is_validate_session:                  
                message = 'Mã phiên giao dịch chưa hợp lệ. Vui lòng nhập lại OTP!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message)  
                
            if session_id != 'stop_trading' and is_validate_session:
                logger.info('Bot BẮT ĐẦU thực hiện trading!')
                trading(user=user, vps_account=vps_account, symbol='All')
                
    except Exception as exc:
        logger.error(f'Error in user_trading_task: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def cancel_trading_task(self, user_id, job_type="morning"):
    """
    Celery task thay thế cho TradingViews.cancel_trading
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f'Job cancel all order is running for {job_type}')
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id
        url = api.TRADING_URL 
        
        cancel_all_orders(user, account_name, account_num, '', url, session_id, '', 'All')
        
    except Exception as exc:
        logger.error(f'Error in cancel_trading_task: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def restart_request_trade_task(self, user_id):
    """
    Celery task thay thế cho TradingViews.restart_request_trade
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info('Job restart all request trade is running')
        ConfigurationOverviewServices.restart_request_trade_overview(user)
        
    except Exception as exc:
        logger.error(f'Error in restart_request_trade_task: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def trading_request_task(self, user_id, stock_id, symbol, request_buy, request_sell, volume_sell):
    """
    Celery task thay thế cho TradingViews.request_trading
    """
    try:
        user = User.objects.get(id=user_id)
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(timezone).time()

        morning_start = time(9, 15)
        morning_end = time(11, 30)
        afternoon_start = time(13, 0)
        afternoon_end = time(14, 28)
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id

        if is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end):
            url = api.TRADING_URL
            res_validate_session = validate_session(account_name, account_num, url, session_id, '')
            
            if not res_validate_session:
                message = 'Session chưa hợp lệ. Bot không thực hiện trading được!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message)  
                return False
                
            if session_id != 'stop_trading' and res_validate_session:
                logger.info('Request trading BẮT ĐẦU thực hiện!')
                
                # Chạy trading_request trong Celery task
                from apps.trading.service.handlers import trading_request
                result = trading_request(user, vps_account, stock_id, symbol, request_buy, request_sell, volume_sell)
                return result
                
        return False
        
    except Exception as exc:
        logger.error(f'Error in trading_request_task: {exc}')
        raise self.retry(exc=exc)
```

---

## 📅 5. Cập nhật Scheduler Logic

### 5.1 Tạo file apps/trading/scheduler/celery_scheduler.py

```python
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
        # 1. User Trading Task - mỗi phút từ 9h-14h
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
```

---

## 🔧 6. Cập nhật Apps.py

### 6.1 Thay thế apps/trading/apps.py

```python
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
```

---

## 🎮 7. Cập nhật Views và API

### 7.1 Cập nhật apps/trading/views.py

```python
# Thêm import
from apps.trading.tasks import user_trading_task, trading_request_task

class TradingViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requests):
        # Thay vì gọi trực tiếp, dispatch task
        user_trading_task.delay(requests.user.id)
        return Response({
            "message": "Trading task đã được dispatch",
            "data": []
        }, status=status.HTTP_200_OK)    

    @staticmethod
    def request_trading(user, stock_id: str, symbol: str, request_buy: bool, request_sell: bool, volume_sell: str):
        # Dispatch Celery task thay vì chạy trực tiếp
        result = trading_request_task.delay(
            user.id, stock_id, symbol, request_buy, request_sell, volume_sell
        )
        return result.get(timeout=30)  # Wait for result
```

### 7.2 Tạo API endpoints mới

```python
# apps/trading/views.py - Thêm các views mới

class StartSchedulerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        from apps.trading.scheduler.celery_scheduler import create_user_schedules
        
        success = create_user_schedules(user)
        if success:
            user.scheduler_status = True
            user.save()
            return Response({"message": f"Scheduler started for user {user.username}!"}, status=200)
        else:
            return Response({"error": "Failed to start scheduler"}, status=500)

class StopSchedulerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        from apps.trading.scheduler.celery_scheduler import remove_user_schedules
        
        success = remove_user_schedules(user)
        if success:
            user.scheduler_status = False
            user.save()
            return Response({"message": f"Scheduler stopped for user {user.username}!"}, status=200)
        else:
            return Response({"error": "Failed to stop scheduler"}, status=500)
```

---

## 🐳 8. Cập nhật Docker Configuration

### 8.1 Cập nhật docker-compose.yml

```yaml
version: '3.8'

services:
  # Existing services...
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery-worker:
    build: .
    command: celery -A config worker -l info -Q trading,trading_high_priority,default
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    environment:
      - DJANGO_ENV=production
      - REDIS_URL=redis://redis:6379/0
    restart: unless-stopped
    deploy:
      replicas: 2  # Scale workers

  celery-beat:
    build: .
    command: celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    environment:
      - DJANGO_ENV=production
      - REDIS_URL=redis://redis:6379/0
    restart: unless-stopped

  celery-flower:  # Optional monitoring
    build: .
    command: celery -A config flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
    restart: unless-stopped

volumes:
  redis_data:
```

### 8.2 Cập nhật Dockerfile

```dockerfile
# Thêm vào Dockerfile
RUN pip install celery redis django-celery-beat django-celery-results
```

---

## 🚀 9. Migration Commands

### 9.1 Tạo migration script

```python
# apps/trading/management/commands/migrate_to_celery.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.trading.scheduler.celery_scheduler import create_user_schedules, remove_user_schedules
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class Command(BaseCommand):
    help = 'Migrate from APScheduler to Celery'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be migrated without doing it')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write("DRY RUN MODE - No changes will be made")
        
        # Get all users with active schedulers
        users_with_scheduler = User.objects.filter(scheduler_status=True)
        
        self.stdout.write(f"Found {users_with_scheduler.count()} users with active schedulers")
        
        for user in users_with_scheduler:
            self.stdout.write(f"Processing user: {user.username}")
            
            if not dry_run:
                # Create Celery schedules
                success = create_user_schedules(user)
                if success:
                    self.stdout.write(f"✅ Created Celery schedules for {user.username}")
                else:
                    self.stdout.write(f"❌ Failed to create Celery schedules for {user.username}")
        
        self.stdout.write("Migration completed!")
```

---

## 📊 10. Monitoring và Debugging

### 10.1 Celery Monitoring Commands

```bash
# Start Celery Worker
celery -A config worker -l info -Q trading,trading_high_priority,default

# Start Celery Beat (Scheduler)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Start Flower (Web UI)
celery -A config flower --port=5555

# Monitor tasks
celery -A config events

# Check worker status
celery -A config inspect active
celery -A config inspect stats
```

### 10.2 Logging Configuration

```python
# settings/base.py - Thêm logging cho Celery

LOGGING = {
    # ... existing config ...
    'loggers': {
        # ... existing loggers ...
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.trading.tasks': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## 🔄 11. Migration Steps

### 11.1 Pre-Migration Checklist

- [ ] Backup database
- [ ] Test Redis connection
- [ ] Verify Celery installation
- [ ] Check Django settings

### 11.2 Migration Process

1. **Install Dependencies**
   ```bash
   pip install celery redis django-celery-beat django-celery-results
   ```

2. **Setup Redis**
   ```bash
   docker-compose up redis -d
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate django_celery_beat
   python manage.py migrate django_celery_results
   ```

4. **Test Celery Setup**
   ```bash
   python manage.py shell
   >>> from apps.trading.tasks import user_trading_task
   >>> result = user_trading_task.delay(1)
   >>> result.get()
   ```

5. **Start Celery Services**
   ```bash
   # Terminal 1: Worker
   celery -A config worker -l info
   
   # Terminal 2: Beat
   celery -A config beat -l info
   ```

6. **Migrate Existing Schedules**
   ```bash
   python manage.py migrate_to_celery
   ```

7. **Stop APScheduler**
   - Comment out APScheduler code
   - Restart Django app

### 11.3 Post-Migration Verification

- [ ] Check Celery worker logs
- [ ] Verify tasks are being scheduled
- [ ] Monitor memory usage
- [ ] Test trading functionality

---

## ⚠️ 12. Rollback Plan

### 12.1 Rollback Steps

1. **Stop Celery Services**
   ```bash
   pkill -f celery
   ```

2. **Restore APScheduler Code**
   - Uncomment APScheduler code
   - Comment out Celery code

3. **Restart Django App**
   ```bash
   python manage.py runserver
   ```

4. **Verify APScheduler Working**
   - Check scheduler logs
   - Test trading functionality

---

## 📈 13. Expected Benefits

### 13.1 Performance Improvements

- **RAM Usage**: Giảm từ 40,000+ threads xuống < 100 processes
- **CPU Usage**: Giảm context switching overhead
- **Memory Leaks**: Eliminated với process-based workers
- **Scalability**: Horizontal scaling với multiple workers

### 13.2 Reliability Improvements

- **Task Persistence**: Tasks không bị mất khi restart
- **Retry Mechanisms**: Auto-retry failed tasks
- **Monitoring**: Better visibility với Flower UI
- **Error Handling**: Improved error tracking và debugging

### 13.3 Operational Benefits

- **Deployment**: Independent scaling của workers
- **Maintenance**: Easier debugging và monitoring
- **Development**: Better local development experience
- **Production**: More robust production setup

---

## 🎯 14. Next Steps

1. **Review** tài liệu này với team
2. **Setup** development environment với Celery
3. **Test** migration trên staging environment
4. **Plan** production migration window
5. **Monitor** performance sau migration

---

## 📞 Support

Nếu có vấn đề trong quá trình migration, hãy check:

1. **Celery Documentation**: https://docs.celeryproject.org/
2. **Django-Celery-Beat**: https://django-celery-beat.readthedocs.io/
3. **Redis Documentation**: https://redis.io/documentation
4. **Logs**: Check Celery worker và beat logs

---

*Tài liệu này được tạo để hỗ trợ migration từ APScheduler sang Celery/RQ cho hệ thống trading scheduler.*
