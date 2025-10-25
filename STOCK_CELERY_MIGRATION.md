# Hướng dẫn Test Celery Tasks cho Stock App

## 1. Chạy Celery Beat và Worker

### Terminal 1 - Celery Beat (Scheduler)
```bash
celery -A config beat -l info
```

### Terminal 2 - Celery Worker
```bash
celery -A config worker -l info
```

## 2. Test Manual Tasks

### Test từ Django Shell
```python
# Mở Django shell
python manage.py shell

# Import tasks
from apps.stock.tasks import (
    download_stock_data_w1_task,
    download_stock_data_d1_task,
    download_stock_data_h1_task,
    download_stock_data_m15_task,
    download_stock_data_m5_task,
    download_stock_data_m1_task,
    delete_old_stock_records_task
)

# Test từng task
result = download_stock_data_d1_task.delay()
print(f"Task ID: {result.id}")

# Test delete old records
result = delete_old_stock_records_task.delay()
print(f"Task ID: {result.id}")
```

### Test từ Command Line
```bash
# Test task cụ thể
celery -A config call apps.stock.tasks.download_stock_data_d1_task

# Xem danh sách tasks
celery -A config inspect registered
```

## 3. Monitor Tasks

### Celery Flower (Web UI)
```bash
celery -A config flower
```
Truy cập: http://localhost:5555

### Celery Events
```bash
celery -A config events
```

## 4. Kiểm tra Scheduled Tasks

### Xem beat schedule
```bash
celery -A config beat --dry-run
```

### Xem active tasks
```bash
celery -A config inspect active
```

## 5. Logs để Debug

### Kiểm tra logs
```bash
# Logs từ Beat
tail -f logs/celery-beat.log

# Logs từ Worker  
tail -f logs/celery-worker.log
```

## 6. Troubleshooting

### Nếu tasks không chạy:
1. Kiểm tra Celery Beat đang chạy
2. Kiểm tra Celery Worker đang chạy
3. Kiểm tra database connection
4. Kiểm tra Redis/RabbitMQ connection

### Nếu có lỗi import:
1. Kiểm tra PYTHONPATH
2. Kiểm tra Django settings
3. Restart Celery services

## 7. Migration từ APScheduler

### Trước (APScheduler):
- Chạy trong Django process
- Sử dụng BackgroundScheduler
- Khởi động trong apps.py

### Sau (Celery Beat):
- Chạy như service riêng biệt
- Sử dụng Celery Beat scheduler
- Tự động retry và error handling
- Scalable và distributed
