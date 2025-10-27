# 🚀 Deploy Final - Scheduler Migration + Redis Fix

## 📋 Tóm tắt thay đổi

### 1. **Trading & Stock Scheduler Migration**
- ✅ Migrate từ APScheduler → Celery Beat + DatabaseScheduler
- ✅ Fix duplicate execution
- ✅ Tự động xử lý duplicate CrontabSchedule/PeriodicTask
- ✅ API endpoint và management command để setup schedules

### 2. **Fix Redis Replica Issue**
- ✅ Thêm redis.conf để force standalone mode
- ✅ Thêm healthcheck cho Redis
- ✅ Tối ưu cấu hình persistence và memory

### 3. **Fix View Authentication**
- ✅ Update `AuthencationStockExchagesView` dùng Celery scheduler
- ✅ Bỏ APScheduler cũ khỏi entrypoint.sh

## 🔄 Các file đã thay đổi

### **Code files:**
1. `apps/trading/scheduler/celery_scheduler.py` - Logic xử lý duplicate
2. `apps/stock/scheduler/celery_scheduler.py` - Migration to Celery Beat
3. `apps/stock/views.py` - Thêm API endpoint setup schedules
4. `apps/stock/urls.py` - Route mới
5. `apps/stock/apps.py` - Đơn giản hóa
6. `apps/authencation_exchange/views.py` - Dùng Celery scheduler
7. `entrypoint.sh` - Bỏ APScheduler restart
8. `config/celery.py` - Update comments

### **Config files:**
9. `docker-compose.yml` - Redis config + healthcheck
10. `redis.conf` - Redis standalone configuration

### **Management commands:**
11. `apps/stock/management/commands/setup_stock_schedules.py`

### **Documentation:**
12. `STOCK_SCHEDULER_GUIDE.md`
13. `DEPLOY_GUIDE.md`
14. `DEPLOY_FINAL.md` (this file)

## 📦 Deploy Steps

### **Step 1: Commit & Push (Local)**

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "feat: Migrate to Celery Beat & Fix Redis replica issue

- Migrate Trading & Stock schedulers from APScheduler to Celery Beat
- Fix duplicate execution với logic tự động xử lý
- Add API endpoint POST /api/stock/setup-schedules
- Add management command setup_stock_schedules
- Fix AuthencationStockExchagesView dùng Celery scheduler
- Add redis.conf force standalone mode
- Add healthcheck cho Redis service
- Update documentation"

# Push
git push origin dev
```

### **Step 2: Deploy on Server**

```bash
# SSH to server
ssh root@minhnguyen-ciqb

# Navigate to project
cd /var/www/AutoBotCk_Backend

# Pull latest code
git pull origin dev

# Stop all services
docker-compose down

# Remove Redis data (để apply redis.conf mới)
docker volume rm autobotck_backend_redis_data

# Build & start
docker-compose build
docker-compose up -d

# Wait for services to be ready
sleep 10
```

### **Step 3: Setup Stock Schedules**

```bash
# Setup via command
docker-compose exec stock-predict-api python manage.py setup_stock_schedules
```

### **Step 4: Verify**

```bash
# Check all services running
docker-compose ps

# Check Redis is standalone (not replica)
docker-compose exec redis redis-cli INFO replication

# Should see:
# role:master
# connected_slaves:0

# Check logs
docker-compose logs -f celery-beat | head -50
```

Bạn sẽ thấy:
- ✅ Trading schedules (2 users × 4 tasks = 8 tasks)
- ✅ Stock schedules (7 tasks)
- ✅ Không còn Redis error

### **Step 5: Test User Login/Logout**

Test endpoint login để verify scheduler được tạo/xóa đúng:

```bash
# Test login
curl -X POST http://localhost:8000/api/authencation-exchange/vps \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "otp": "123456",
    "isTrading": false
  }'

# Check logs - không còn lỗi "Không tìm thấy Scheduler"
docker-compose logs -f stock-predict-api
```

## ✅ Success Criteria

Sau khi deploy thành công:

- [ ] Redis role = master (không còn replica)
- [ ] Celery Beat logs hiển thị cả Trading và Stock tasks
- [ ] Không còn error "UNBLOCKED force unblock"
- [ ] Không còn warning "Không tìm thấy Scheduler"
- [ ] User login/logout hoạt động bình thường
- [ ] Bot chạy đúng 1 lần (không duplicate)
- [ ] Stock data được download đều đặn

## 🐛 Troubleshooting

### Redis vẫn là replica?
```bash
# Force reset về master
docker-compose exec redis redis-cli
> REPLICAOF NO ONE
> INFO replication
> exit

docker-compose restart redis
```

### Stock schedules chưa được tạo?
```bash
docker-compose exec stock-predict-api python manage.py setup_stock_schedules
```

### Celery worker crash?
```bash
# Check logs
docker-compose logs celery-worker | tail -100

# Restart
docker-compose restart celery-worker
```

## 📊 Monitor

Sau deploy, monitor trong 1-2 giờ:

```bash
# Realtime logs
docker-compose logs -f celery-beat celery-worker

# Check tasks chạy
docker-compose logs celery-worker | grep -i "succeeded\|failed"

# Check Redis memory
docker-compose exec redis redis-cli INFO memory
```

## 🎯 Rollback (nếu cần)

```bash
cd /var/www/AutoBotCk_Backend
git log --oneline -5
git checkout <previous_commit_hash>
docker-compose down
docker-compose up -d
```

## 📞 Support

Nếu có vấn đề:
1. Check logs: `docker-compose logs -f`
2. Check Redis: `docker-compose exec redis redis-cli INFO`
3. Check database schedules: Django Admin → Periodic Tasks
4. Check Flower: http://localhost:5555/

---

**Note:** Lần deploy này sẽ **xóa Redis data cũ** (để apply config mới). Celery tasks sẽ tự động recreate trong database nên không mất dữ liệu quan trọng.

