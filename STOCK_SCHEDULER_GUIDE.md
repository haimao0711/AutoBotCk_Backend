# Stock Scheduler Migration Guide

## ✅ Đã hoàn thành

APScheduler đã được thay thế hoàn toàn bằng **Celery Beat + DatabaseScheduler**.

## 📁 Các file đã thay đổi

### 1. **apps/stock/scheduler/celery_scheduler.py**
- Chuyển từ `app.conf.beat_schedule` (không hoạt động với DatabaseScheduler)
- Sang `PeriodicTask` trong database (tương tự Trading scheduler)
- Có logic xử lý duplicate tự động

### 2. **apps/stock/apps.py**
- Tự động gọi `setup_stock_schedules()` khi Celery Beat khởi động
- Delay 5 giây để đảm bảo database đã sẵn sàng

### 3. **config/celery.py**
- Bỏ logic setup không cần thiết
- Thêm comment giải thích cách hoạt động

### 4. **apps/stock/scheduler/stock_imported.py**
- Đánh dấu DEPRECATED
- File này KHÔNG còn được sử dụng

## 🚀 Cách sử dụng

### Option 1: Qua API Endpoint (Khuyến nghị)
```bash
POST /api/stock/setup-schedules

# Ví dụ với curl:
curl -X POST http://localhost:8000/api/stock/setup-schedules \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# Response:
{
  "success": true,
  "message": "✅ Stock schedules setup completed successfully!",
  "schedules": [
    "delete_old_stock_records",
    "download_stock_data_w1",
    "download_stock_data_d1",
    "download_stock_data_h1",
    "download_stock_data_m15",
    "download_stock_data_m5",
    "download_stock_data_m1"
  ]
}
```

### Option 2: Qua Management Command
```bash
# Trong Docker
docker-compose exec stock-predict-api python manage.py setup_stock_schedules

# Hoặc local
python manage.py setup_stock_schedules
```

## 📋 Danh sách schedules

Tất cả 7 tasks sẽ được tạo trong database:

| Task Name | Schedule | Description |
|-----------|----------|-------------|
| `delete_old_stock_records` | Hàng giờ từ 9:00-15:00 | Xóa dữ liệu cũ |
| `download_stock_data_w1` | Thứ 2 hàng tuần lúc 9:00 | Download dữ liệu tuần |
| `download_stock_data_d1` | Hàng ngày lúc 9:00 | Download dữ liệu ngày |
| `download_stock_data_h1` | Hàng giờ từ 9:00-15:00 | Download dữ liệu giờ |
| `download_stock_data_m15` | Mỗi 15 phút từ 9:00-15:00 | Download dữ liệu 15 phút |
| `download_stock_data_m5` | Mỗi 5 phút từ 9:00-15:00 | Download dữ liệu 5 phút |
| `download_stock_data_m1` | Mỗi phút từ 9:00-15:00 | Download dữ liệu 1 phút |

## 🔍 Kiểm tra schedules

### Trong logs
```bash
docker-compose logs celery-beat | grep -i stock
```

Bạn sẽ thấy:
```
📅 Stock schedules will be initialized in 5 seconds...
🔄 Creating Stock data download schedules in database...
✅ Stock schedules created successfully!
```

### Trong database
```bash
docker-compose exec stock-predict-api python manage.py shell
```

```python
from django_celery_beat.models import PeriodicTask

# Xem tất cả Stock tasks
stock_tasks = PeriodicTask.objects.filter(name__startswith='download_stock_data')
for task in stock_tasks:
    print(f"{task.name}: {task.crontab} - Enabled: {task.enabled}")
```

### Trong Flower UI
Truy cập: http://localhost:5555/

## ⚠️ Lưu ý

1. **Không dùng APScheduler nữa**: File `stock_imported.py` đã deprecated
2. **DatabaseScheduler**: Schedules được lưu trong database, không phải code
3. **Duplicate handling**: Code tự động xử lý duplicate schedules
4. **Timezone**: Tất cả schedules dùng `Asia/Ho_Chi_Minh`

## 🐛 Troubleshooting

### Không thấy Stock schedules trong logs?
```bash
# Restart Celery Beat
docker-compose restart celery-beat

# Xem logs đầy đủ
docker-compose logs celery-beat | tail -200
```

### Muốn xóa và tạo lại schedules?
```bash
docker-compose exec stock-predict-api python manage.py shell
```

```python
from django_celery_beat.models import PeriodicTask

# Xóa tất cả Stock schedules
PeriodicTask.objects.filter(name__contains='stock_data').delete()
PeriodicTask.objects.filter(name='delete_old_stock_records').delete()

# Chạy lại setup
from apps.stock.scheduler.celery_scheduler import setup_stock_schedules
setup_stock_schedules()
```

### Schedules không chạy?
1. Kiểm tra Celery Worker đang chạy: `docker-compose ps`
2. Kiểm tra Celery Beat đang chạy: `docker-compose logs celery-beat`
3. Kiểm tra task enabled: Django Admin → Periodic Tasks
4. Kiểm tra timezone đúng không

## ✨ So sánh với Trading Scheduler

| Aspect | Stock Scheduler | Trading Scheduler |
|--------|----------------|-------------------|
| Type | Static schedules | Dynamic per-user |
| Created | At startup | When user enables bot |
| Count | 7 tasks (fixed) | 4 tasks × N users |
| Managed by | System | Users (on/off) |

