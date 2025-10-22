# PgBouncer Deployment Guide

## Files đã được cập nhật:

1. **docker-compose.yml** - Thêm PgBouncer service
2. **pgbouncer.ini** - Cấu hình PgBouncer
3. **userlist.txt** - User authentication cho PgBouncer
4. **config/settings/base.py** - Cập nhật database config
5. **config/settings/production.py** - Cập nhật production settings

## Environment Variables cần thiết:

Tạo file `.env.production` với nội dung:
```
DJANGO_ENV=production
POSTGRES_DB=stockdb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=pgbouncer
POSTGRES_PORT=6432
DEBUG=False
SECRET_KEY=your-secret-key-here
```

## Deploy trên VPS:

1. **Pull code mới:**
   ```bash
   git pull origin dev
   ```

2. **Build và restart services:**
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

3. **Kiểm tra logs:**
   ```bash
   docker-compose logs -f pgbouncer
   docker-compose logs -f stock-predict-api
   ```

## Kiểm tra PgBouncer hoạt động:

```bash
# Kết nối đến PgBouncer admin
docker-compose exec pgbouncer psql -h localhost -p 6432 -U myuser -d pgbouncer

# Xem stats
docker-compose exec pgbouncer psql -h localhost -p 6432 -U myuser -d pgbouncer -c "SHOW STATS;"
```

## Rollback nếu cần:

Nếu có vấn đề, chỉ cần đổi lại:
- `POSTGRES_HOST=stock-predict-postgres`
- `POSTGRES_PORT=5432`
- Restart services
