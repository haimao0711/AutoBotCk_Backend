# Hướng dẫn: Đảm bảo `is_trading` luôn tắt khi có lỗi

Để đảm bảo trạng thái `is_trading` không bị treo (stuck) ở `True` khi có lỗi hoặc sự cố, chúng ta cần tiếp cận theo 2 lớp bảo vệ:

## Lớp 1: Bảo vệ ở mức Code (Function Level)

Hiện tại, logic tắt `is_trading` đang nằm rải rác ở cuối hàm hoặc trong block `except`. Nếu hàm bị `return` sớm hoặc lỗi xảy ra ở những chỗ không ngờ tới, trạng thái sẽ bị treo.

**Giải pháp:** Chuyển logic reset `is_trading` vào block `finally`. Block `finally` **luôn luôn** được thực thi bất kể hàm kết thúc thành công, gặp lỗi, hay có lệnh `return`.

### Cách thực hiện:

Sửa hàm `process_trading` như sau:

```python
def process_trading(...):
    stock_id = None
    try:
        # ... logic lấy stock_id ...
        stock_id = trading_config.stock_id 
        
        # ... Toàn bộ logic trading ...

    except Exception as e:
        logger.error(f"Lỗi: {e}")
        # Không cần reset ở đây nữa, để finally lo
    finally:
        # Logic này SẼ LUÔN CHẠY
        if stock_id:
            try:
                # 1. Kiểm tra xem có đang Mua/Bán tay không
                is_manual = check_manual_status(user, symbol) 
                
                # 2. Nếu không phải Mua/Bán tay, thì tắt is_trading
                if not is_manual:
                     ConfigurationServices.update_is_trading_configuration(user, stock_id, False)
                     logger.info(f"Đã reset is_trading cho {symbol}")
                else:
                     logger.info(f"Giữ is_trading cho {symbol} do đang Mua/Bán tay")
            except Exception as final_e:
                logger.error(f"Lỗi cực nghiêm trọng trong finally: {final_e}")
        
        connection.close()
```

## Lớp 2: Bảo vệ ở mức Hệ thống (System Level) - Watchdog

Nếu Server bị crash (mất điện, kill process), code `finally` cũng **không thể chạy**. Đây là nguyên nhân chính gây ra "bot chết nhưng trạng thái vẫn active".

**Giải pháp:** Tạo một **Watchdog Job** (chạy nền 5-10 phút/lần).

### Cách thực hiện:
Viết một script hoặc Cronjob thực hiện logic sau:
1.  Quét DB lấy danh sách tất cả các mã đang có `is_trading = True`.
2.  Kiểm tra thời gian cập nhật cuối cùng (`updated_at` hoặc heartbeat).
3.  Nếu `is_trading = True` mà quá **30 phút** không có cập nhật gì -> **Cưỡng chế set False**.

---

## Bạn có muốn tôi thực hiện Lớp 1 (Sửa code `finally` trong `handlers.py`) ngay bây giờ không?
Việc này sẽ giải quyết được 95% các trường hợp treo trạng thái do lỗi phần mềm (Exception).
