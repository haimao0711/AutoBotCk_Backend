# 🔒 Hướng dẫn sửa lỗi SSL Certificate - ERR_CERT_DATE_INVALID

## ❌ Lỗi hiện tại
```
Your connection is not private
Attackers might be trying to steal your information from autobotchungkhoan.pro.vn
net::ERR_CERT_DATE_INVALID
```

## 🔍 Nguyên nhân
Lỗi này xảy ra khi:
1. **SSL certificate đã hết hạn** (phổ biến nhất)
2. **SSL certificate chưa được cấu hình** trên nginx
3. **Date/time trên server không đúng**
4. **Certificate không khớp với domain**

## ✅ Các bước kiểm tra và sửa lỗi

### **Bước 1: SSH vào server và kiểm tra date/time**

```bash
# SSH vào server
ssh root@minhnguyen-ciqb

# Kiểm tra date/time hiện tại
date

# Nếu date/time sai, đồng bộ lại:
timedatectl set-ntp true
# hoặc
ntpdate -s time.nist.gov
```

### **Bước 2: Kiểm tra cấu hình nginx**

```bash
# Tìm file cấu hình nginx cho domain
ls -la /etc/nginx/sites-available/
ls -la /etc/nginx/sites-enabled/

# Xem cấu hình hiện tại
cat /etc/nginx/sites-available/autobotchungkhoan.pro.vn
# hoặc
cat /etc/nginx/conf.d/autobotchungkhoan.pro.vn.conf
```

### **Bước 3: Kiểm tra SSL certificate hiện tại**

```bash
# Kiểm tra certificate đã được cấu hình chưa
openssl s_client -connect autobotchungkhoan.pro.vn:443 -servername autobotchungkhoan.pro.vn < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Hoặc kiểm tra trực tiếp
echo | openssl s_client -servername autobotchungkhoan.pro.vn -connect autobotchungkhoan.pro.vn:443 2>/dev/null | openssl x509 -noout -dates
```

Kết quả sẽ hiển thị:
- `notBefore`: Ngày bắt đầu có hiệu lực
- `notAfter`: Ngày hết hạn

### **Bước 4: Cài đặt/cập nhật SSL certificate**

Có 2 cách phổ biến:

#### **Option A: Sử dụng Let's Encrypt (Free, khuyến nghị)**

```bash
# Cài đặt certbot nếu chưa có
apt-get update
apt-get install -y certbot python3-certbot-nginx

# Lấy certificate mới
certbot --nginx -d autobotchungkhoan.pro.vn -d www.autobotchungkhoan.pro.vn

# Hoặc nếu đã có certificate nhưng hết hạn, renew:
certbot renew

# Test auto-renewal
certbot renew --dry-run
```

#### **Option B: Sử dụng certificate từ nhà cung cấp**

Nếu bạn có certificate từ nhà cung cấp domain:

```bash
# Tạo thư mục chứa certificate
mkdir -p /etc/nginx/ssl/autobotchungkhoan.pro.vn

# Copy certificate files vào (thay bằng đường dẫn thực tế của bạn)
# cp your-certificate.crt /etc/nginx/ssl/autobotchungkhoan.pro.vn/
# cp your-private-key.key /etc/nginx/ssl/autobotchungkhoan.pro.vn/
# cp your-ca-bundle.crt /etc/nginx/ssl/autobotchungkhoan.pro.vn/
```

### **Bước 5: Cấu hình nginx với SSL**

Tạo hoặc cập nhật file cấu hình nginx:

```bash
# Tạo file cấu hình
nano /etc/nginx/sites-available/autobotchungkhoan.pro.vn
```

Nội dung file cấu hình (ví dụ với Let's Encrypt):

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name autobotchungkhoan.pro.vn www.autobotchungkhoan.pro.vn;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name autobotchungkhoan.pro.vn www.autobotchungkhoan.pro.vn;

    # SSL certificate (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/autobotchungkhoan.pro.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/autobotchungkhoan.pro.vn/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to Django backend
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    # Static files (nếu có)
    location /static/ {
        alias /var/www/AutoBotCk_Backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    access_log /var/log/nginx/autobotchungkhoan.pro.vn.access.log;
    error_log /var/log/nginx/autobotchungkhoan.pro.vn.error.log;
}
```

Nếu dùng certificate từ nhà cung cấp, thay đổi các dòng SSL:

```nginx
ssl_certificate /etc/nginx/ssl/autobotchungkhoan.pro.vn/your-certificate.crt;
ssl_certificate_key /etc/nginx/ssl/autobotchungkhoan.pro.vn/your-private-key.key;
# Nếu có CA bundle:
# ssl_trusted_certificate /etc/nginx/ssl/autobotchungkhoan.pro.vn/your-ca-bundle.crt;
```

### **Bước 6: Enable site và test cấu hình**

```bash
# Enable site (nếu chưa enable)
ln -s /etc/nginx/sites-available/autobotchungkhoan.pro.vn /etc/nginx/sites-enabled/

# Test cấu hình nginx
nginx -t

# Nếu test thành công, reload nginx
systemctl reload nginx
# hoặc
service nginx reload
```

### **Bước 7: Kiểm tra lại**

```bash
# Kiểm tra certificate mới
openssl s_client -connect autobotchungkhoan.pro.vn:443 -servername autobotchungkhoan.pro.vn < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Kiểm tra từ browser
# Truy cập: https://autobotchungkhoan.pro.vn
```

### **Bước 8: Thiết lập auto-renewal (cho Let's Encrypt)**

Let's Encrypt certificate hết hạn sau 90 ngày. Thiết lập auto-renewal:

```bash
# Kiểm tra cron job đã có chưa
crontab -l | grep certbot

# Nếu chưa có, thêm vào:
crontab -e

# Thêm dòng này (chạy 2 lần mỗi ngày để đảm bảo)
0 0,12 * * * certbot renew --quiet --deploy-hook "systemctl reload nginx"
```

## 🔧 Troubleshooting

### **Lỗi: "certbot: command not found"**
```bash
apt-get update
apt-get install -y certbot python3-certbot-nginx
```

### **Lỗi: "nginx: command not found"**
```bash
apt-get update
apt-get install -y nginx
```

### **Lỗi: "Port 80/443 already in use"**
```bash
# Kiểm tra process đang dùng port
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# Dừng service đang dùng port (thường là apache2)
systemctl stop apache2
systemctl disable apache2
```

### **Lỗi: "Domain verification failed"**
- Đảm bảo domain trỏ đúng về IP server
- Đảm bảo port 80 và 443 đã mở trong firewall
- Kiểm tra DNS: `nslookup autobotchungkhoan.pro.vn`

### **Certificate vẫn hiển thị lỗi sau khi cài đặt**
1. Clear browser cache
2. Thử truy cập ở chế độ incognito
3. Kiểm tra lại date/time trên server
4. Kiểm tra nginx đã reload chưa: `systemctl status nginx`

## 📝 Checklist

- [ ] Date/time trên server đúng
- [ ] Nginx đã được cài đặt
- [ ] SSL certificate đã được cài đặt (Let's Encrypt hoặc từ nhà cung cấp)
- [ ] File cấu hình nginx đã được tạo và enable
- [ ] `nginx -t` không có lỗi
- [ ] Nginx đã được reload
- [ ] Certificate không hết hạn (kiểm tra bằng openssl)
- [ ] Truy cập https://autobotchungkhoan.pro.vn không còn lỗi
- [ ] Auto-renewal đã được thiết lập (nếu dùng Let's Encrypt)

## 🆘 Cần hỗ trợ?

Nếu vẫn gặp vấn đề, cung cấp thông tin sau:
1. Output của `nginx -t`
2. Output của `openssl s_client -connect autobotchungkhoan.pro.vn:443`
3. Nginx error logs: `tail -50 /var/log/nginx/error.log`
4. Nginx config file hiện tại



