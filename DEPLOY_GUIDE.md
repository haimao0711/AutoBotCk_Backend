# 🚀 Hướng dẫn Deploy Code

## 📝 Tóm tắt thay đổi

### 1. **Trading Scheduler - Fix duplicate execution**
- ✅ Xử lý duplicate PeriodicTask và CrontabSchedule
- ✅ Logic thông minh: tự động phát hiện và dọn dẹp
- ✅ Giữ nguyên 2 Celery workers

### 2. **Stock Scheduler - Migration to Celery Beat**
- ✅ Chuyển từ APScheduler sang Celery Beat + DatabaseScheduler
- ✅ Thêm API endpoint và management command để setup schedules
- ✅ File `stock_imported.py` đã deprecated

## 🔄 Quy trình Deploy

### **Bước 1: Local - Commit & Push**
```bash
# Xem những file đã thay đổi
git status

# Add tất cả thay đổi
git add .

# Commit với message rõ ràng
git commit -m "Fix: Trading duplicate execution & Migrate Stock to Celery Beat"

# Push lên remote
git push origin dev
```

### **Bước 2: Server - Pull & Build**
```bash
# SSH vào server
ssh root@minhnguyen-ciqb

# Vào thư mục project
cd /var/www/AutoBotCk_Backend

# Stash local changes nếu có (hoặc commit local changes trước)
git stash

# Pull code mới
git pull origin dev

# Apply stash nếu cần
git stash pop

# Build lại Docker images
docker-compose build

# Restart services
docker-compose down
docker-compose up -d

# Xem logs để kiểm tra
docker-compose logs -f celery-beat
```

### **Bước 3: Setup Stock Schedules**

Sau khi services chạy, setup Stock schedules:

#### **Option A: Qua API (Khuyến nghị)**
```bash
# Lấy token từ login
TOKEN="your_token_here"

# Gọi API setup schedules
curl -X POST http://localhost:8000/api/stock/setup-schedules \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

#### **Option B: Qua Management Command**
```bash
docker-compose exec stock-predict-api python manage.py setup_stock_schedules
```

### **Bước 4: Kiểm tra logs**

```bash
# Xem logs Celery Beat
docker-compose logs -f celery-beat

# Bạn sẽ thấy:
# - Trading schedules cho users
# - Stock schedules (7 tasks)
```

## ✅ Checklist sau khi deploy

- [ ] Services đang chạy: `docker-compose ps`
- [ ] Celery Beat logs không có lỗi
- [ ] Celery Workers đang hoạt động
- [ ] Trading tasks vẫn chạy bình thường
- [ ] Stock schedules đã được tạo (7 tasks)
- [ ] Không còn duplicate execution

## 🔍 Verify Stock Schedules

### Trong database:
```bash
docker-compose exec stock-predict-api python manage.py shell
```

```python
from django_celery_beat.models import PeriodicTask

# Xem Stock tasks
stock_tasks = PeriodicTask.objects.filter(
    name__in=[
        'delete_old_stock_records',
        'download_stock_data_w1',
        'download_stock_data_d1',
        'download_stock_data_h1',
        'download_stock_data_m15',
        'download_stock_data_m5',
        'download_stock_data_m1'
    ]
)

for task in stock_tasks:
    print(f"✅ {task.name}: {task.enabled}")

# Kết quả mong đợi: 7 tasks enabled=True
```

### Trong logs (sau khi đến giờ chạy):
```bash
docker-compose logs celery-worker | grep -i "stock"

# Sẽ thấy:
# Celery job download M1 is running...
# Celery job download M5 is running...
# ...
```

## ⚠️ Troubleshooting

### 1. Stock schedules không được tạo?
```bash
# Gọi lại API hoặc command
docker-compose exec stock-predict-api python manage.py setup_stock_schedules
```

### 2. Trading tasks vẫn chạy 2 lần?
```bash
# Xem có duplicate không
docker-compose exec stock-predict-api python manage.py shell
```
```python
from django_celery_beat.models import PeriodicTask

# Tìm duplicate
from collections import Counter
task_names = PeriodicTask.objects.values_list('name', flat=True)
duplicates = [name for name, count in Counter(task_names).items() if count > 1]
print("Duplicates:", duplicates)

# Xóa duplicate và tạo lại
if duplicates:
    from apps.trading.scheduler.celery_scheduler import restart_all_user_schedules
    restart_all_user_schedules()
```

### 3. Celery Beat không start?
```bash
# Check logs
docker-compose logs celery-beat | tail -100

# Restart
docker-compose restart celery-beat
```

## 📊 Expected Behavior sau deploy

### Trading Scheduler:
- ✅ Mỗi user chỉ có 4 tasks
- ✅ Tasks chạy đúng schedule (mỗi phút, 11:29, 14:29, 14:30)
- ✅ Không còn duplicate execution
- ✅ Logic tự động dọn dẹp duplicate

### Stock Scheduler:
- ✅ Có 7 tasks trong database
- ✅ Tasks chạy đúng schedule (W1, D1, H1, M15, M5, M1)
- ✅ APScheduler đã không còn được sử dụng
- ✅ Có thể tái tạo schedules qua API/command bất cứ lúc nào

## 🎯 Next Steps

1. Monitor logs trong vài giờ đầu
2. Kiểm tra xem Stock data có được download không
3. Kiểm tra Trading bot vẫn hoạt động bình thường
4. Nếu ổn định, có thể xóa file deprecated: `apps/stock/scheduler/stock_imported.py`

## 📞 Support

Nếu có vấn đề, check:
1. Logs: `docker-compose logs -f`
2. Database schedules: Django Admin → Periodic Tasks
3. Flower UI: http://localhost:5555/

