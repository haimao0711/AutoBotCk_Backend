 # Báo cáo Phân tích Rủi ro hàm `process_trading`

Dưới đây là các nguy cơ tiềm ẩn gây treo luồng (thread hanging) và treo trạng thái (stuck state) được phát hiện trong hàm `process_trading` tại file `apps/trading/service/handlers.py`.

## 1. Nguy cơ Treo Luồng (Thread Hanging) - Rủi ro cao

### Vấn đề:
Hệ thống sử dụng `ThreadPoolExecutor` với giới hạn `max_workers=100` (dòng 2373). Tuy nhiên, hàm `process_trading` chứa các vòng lặp chờ đợi kéo dài (long-running blocking loops):

1.  **Vòng lặp Chốt lời (Take Profit Loop)** (Dòng 1965 - 2009):
    *   Điều kiện: `while datetime.now() < end_time:`
    *   Thời gian chờ: **5 giờ** (`timedelta(hours=5)` tại dòng 1963).
    *   Hành vi: Thread sẽ bị block trong tối đa 5 giờ, chỉ ngủ 30s (`time.sleep(30)`) rồi lặp lại.

2.  **Vòng lặp Mua/Bán Tay (Manual Request Loops)** (Trong `process_buy/sell_request`, được gọi gián tiếp hoặc tương tự):
    *   Thời gian chờ: **2 giờ**.

### Hậu quả:
Nếu có hơn 100 mã cổ phiếu (trên tất cả user) rơi vào trạng thái chờ "Chốt lời" hoặc "Mua/Bán tay" cùng lúc:
*   Toàn bộ 100 worker threads sẽ bị chiếm dụng.
*   **Hệ thống bị tê liệt**: Các mã chứng khoán khác cần xử lý (mua/bán thường) sẽ phải xếp hàng chờ đợi cho đến khi một trong các thread kia thoát (có thể tới 5 giờ).
*   Gây trễ lệnh nghiêm trọng cho toàn bộ hệ thống.

## 2. Nguy cơ Treo Trạng thái (Stuck State / Dirty State)

### Vấn đề A: Trạng thái `is_trading` bị kẹt
*   **Cơ chế**: Hàm set `is_trading = True` khi bắt đầu chốt lời (dòng 1959) và dự kiến set `False` trong khối `finally` (dòng 2291) hoặc `except` (dòng 2288).
*   **Rủi ro**: Nếu tiến trình (process) bị dừng đột ngột (Server restart, Crash, OOM Kill, Deployment) trong suốt thời gian chờ 5 giờ:
    *   Khối `finally` **không được thực thi**.
    *   Database vẫn lưu `is_trading = True` cho mã đó.
    *   **Hậu quả**: Bot sẽ bỏ qua mã này trong các lần chạy sau (do cơ chế lọc `is_trading`), khiến mã bị "liệt" vĩnh viễn cho đến khi can thiệp database thủ công.

### Vấn đề B: Cấu hình "bóng ma" (Stale Configuration)
*   **Chi tiết**: Trong vòng lặp 5 giờ (dòng 1965):
    *   Code tải lại dữ liệu thị trường (`download_data`).
    *   Nhưng **KHÔNG tải lại cấu hình user** (`trading_config`, `overview_config`).
    *   Biến `trading_config` vẫn giữ giá trị từ lúc bắt đầu hàm (có thể là 4 giờ trước).
*   **Hậu quả**:
    *   Nếu user **Tắt Bot** hoặc **Thay đổi điểm chốt lời** trong lúc thread đang chờ, Bot **không hề hay biết** và vẫn hành động theo cấu hình cũ.
    *   Dẫn đến việc bán sai, hoặc bán khi user đã yêu cầu dừng.

## 3. Khuyến nghị Sửa chữa

1.  **Loại bỏ vòng lặp `while` kéo dài**:
    *   Thay vì giữ thread chờ 5 tiếng, hãy thiết kế theo cơ chế **Polling (Kiểm tra định kỳ)**.
    *   Chạy xong 1 lần kiểm tra -> Thoát hàm -> Trả lại Thread.
    *   Lần chạy Job tiếp theo (sau 30s/1p) sẽ kiểm tra lại điều kiện tiếp.

2.  **Refresh Config trong vòng lặp (nếu buộc phải giữ vòng lặp)**:
    *   Phải gọi `ConfigurationServices` để lấy config mới nhất trong mỗi bước lặp để đảm bảo tuân thủ lệnh dừng của user.

3.  **Cơ chế Timeout/Heartbeat cho `is_trading`**:
    *   Cần có cơ chế reset `is_trading` nếu nó đã bật quá lâu (ví dụ: Job dọn dẹp).
