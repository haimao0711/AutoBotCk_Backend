# VPS API Local Proxy

## Vấn đề
Server VPS (Linux/datacenter) bị WAF của VPS Securities chặn.  
Máy local (Windows) vẫn gọi được API bình thường.

## Giải pháp
Chạy proxy server nhỏ trên máy Windows local.  
Django server gọi proxy → proxy forward lên `bgapi.vps.com.vn`.

```
[Docker Server] → [Local Proxy :9000] → [bgapi.vps.com.vn]
```

## Cách chạy

### 1. Cài dependencies (chỉ làm 1 lần)
```powershell
pip install flask requests
```

### 2. Chạy proxy
```powershell
cd e:\ANguyenBot\stock-predict-cms-be\local_proxy
python vps_proxy_server.py
# hoặc chỉ định port khác:
python vps_proxy_server.py 9001
```

### 3. Lấy IP máy Windows (để cấu hình server)
```powershell
ipconfig | Select-String "IPv4"
```

### 4. Cấu hình server Linux

Thêm vào file `.env.production` trên server:
```
VPS_PROXY_URL=http://<IP_MÁY_WINDOWS>:9000
```

Sau đó restart Docker:
```bash
docker-compose restart stock-predict-api celery-worker celery-beat
```

## Lưu ý bảo mật
- Chỉ mở port 9000 cho IP của server Linux, không mở public
- Có thể dùng Windows Firewall để giới hạn:
  ```powershell
  # Chỉ cho phép IP server kết nối vào port 9000
  New-NetFirewallRule -DisplayName "VPS Proxy" -Direction Inbound -Protocol TCP -LocalPort 9000 -RemoteAddress <SERVER_IP> -Action Allow
  ```

