from apps.stock.models import Stock
from apps.configuration.candle.enums import CandleEnum
from apps.stock.enums import DownloadStatusEnum
from apps.stock.services import DownloadService
from apps.trading.service.helper import adding_idicator
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import threading
import time

class VNIndexManager:
    """
    Quản lý Cache dữ liệu VNINDEX để tránh tải và tính toán lại nhiều lần trong các luồng.
    Sử dụng cơ chế TTL (Time To Live) và Locking để đảm bảo thread-safe.
    """
    _cache = {}  # {chart_type: {"data": df, "timestamp": float}}
    _lock = threading.Lock()
    _ttl = 60  # Cache có hiệu lực trong 60 giây

    @classmethod
    def get_data(cls, vnindex_stock, chart_type):
        now = time.time()
        
        # 1. Kiểm tra cache trước (không cần lock để nhanh)
        cache_entry = cls._cache.get(chart_type)
        if cache_entry and (now - cache_entry["timestamp"] < cls._ttl):
            # logger.info(f"VNINDEX Cache Hit: {chart_type}")
            return cache_entry["data"].copy()

        # 2. Nếu hết hạn hoặc chưa có, dùng lock để chỉ 1 luồng đi fetch
        with cls._lock:
            # Check lại một lần nữa sau khi có lock (Double-checked locking)
            cache_entry = cls._cache.get(chart_type)
            if cache_entry and (now - cache_entry["timestamp"] < cls._ttl):
                return cache_entry["data"].copy()

            # Thực hiện tải mới
            try:
                from apps.trading.service.handlers import logger # Late import to avoid circular dependency
                # logger.info(f"VNINDEX Cache Miss/Expired: Refreshing {chart_type}...")
                
                df = DownloadService.download_data_single(
                    stock=vnindex_stock, 
                    chart_type=chart_type, 
                    download_status=DownloadStatusEnum.NEW.value
                )
                
                # Patch realtime data
                vnindex_info = DownloadService.get_stock_info(vnindex_stock.symbol, None)
                if vnindex_info and 'matchPrice' in vnindex_info:
                    patch_realtime_data(df, vnindex_info['matchPrice'], chart_type)
                
                # Tính toán chỉ số
                adding_idicator(df)
                
                # Cập nhật cache
                cls._cache[chart_type] = {
                    "data": df,
                    "timestamp": time.time()
                }
                return df.copy()
            except Exception as e:
                print(f"Error refreshing VNINDEX cache for {chart_type}: {e}")
                # Nếu lỗi và có cache cũ, dùng tạm cache cũ thay vì crash
                if cache_entry:
                    return cache_entry["data"].copy()
                return None

    @classmethod
    def clear_cache(cls):
        with cls._lock:
            cls._cache.clear()

def download_data_stock_only(stock: Stock, trading_chart_type: CandleEnum, following_chart_type: CandleEnum):
    """
    Chỉ tải dữ liệu cho Stock cụ thể, không tải VNINDEX.
    """
    try:
        stock_data_following = DownloadService.download_data_single(
            stock=stock, chart_type=following_chart_type, download_status=DownloadStatusEnum.NEW.value)
        stock_data_trading = DownloadService.download_data_single(
            stock=stock, chart_type=trading_chart_type, download_status=DownloadStatusEnum.NEW.value)
        
        # Patch realtime data for Stock
        try:
            stock_info = DownloadService.get_stock_info(stock.symbol, None)
            if stock_info and 'matchPrice' in stock_info:
                match_price = stock_info['matchPrice']
                patch_realtime_data(stock_data_following, match_price, following_chart_type)
                patch_realtime_data(stock_data_trading, match_price, trading_chart_type)
        except Exception as e:
            print(f"Error patching Stock realtime data: {e}")

        adding_idicator(stock_data_following)
        adding_idicator(stock_data_trading)
        
        return stock_data_trading, stock_data_following
    except Exception as e:
        print(f"Error in download_data_stock_only for {stock.symbol}: {e}")
        return None, None

def patch_realtime_data(df, match_price, chart_type):
    if df is None or df.empty:
        return

    try:
        # timezone
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(tz)
        
        chart_type_val = chart_type.value if isinstance(chart_type, CandleEnum) else chart_type
        
        if chart_type_val == CandleEnum.W1.value:
            # Chuyển sang naive để tránh cảnh báo từ Pandas khi dùng to_period
            now_naive = now.replace(tzinfo=None)
            start_time_naive = pd.Timestamp(now_naive).to_period('W-SUN').start_time
            # Gán lại timezone để tính timestamp() chính xác
            start_time = tz.localize(start_time_naive)
        elif chart_type_val == CandleEnum.D1.value:
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif chart_type_val == CandleEnum.H1.value:
            start_time = now.replace(minute=0, second=0, microsecond=0)
        elif chart_type_val == CandleEnum.M15.value:
            minute = (now.minute // 15) * 15
            start_time = now.replace(minute=minute, second=0, microsecond=0)
        elif chart_type_val == CandleEnum.M5.value:
            minute = (now.minute // 5) * 5
            start_time = now.replace(minute=minute, second=0, microsecond=0)
        elif chart_type_val == CandleEnum.M1.value:
            start_time = now.replace(second=0, microsecond=0)
        
        if start_time is None:
            return

        # Đảm bảo start_time là naive timestamp đại diện cho giờ VN để khớp với hệ thống (ngoại trừ W1)
        if chart_type_val != CandleEnum.W1.value:
            if hasattr(start_time, 'tzinfo') and start_time.tzinfo is not None:
                start_time = start_time.replace(tzinfo=None)
            
        current_candle_ts = int(start_time.timestamp())
        
        last_idx = df.index[-1]
        
        # --- Normalization Logic ---
        last_close = df.at[last_idx, 'close']
        if last_close > 0:
            ratio = match_price / last_close
            if ratio > 100:
                match_price = match_price / 1000
            elif ratio < 0.01:
                match_price = match_price * 1000
        # ---------------------------

        # Tìm xem trong df đã có nến cho mốc thời gian này chưa
        # (Sử dụng list index để an toàn)
        existing_indices = df.index[df['time'].astype(int) == current_candle_ts].tolist()
        
        if existing_indices:
            idx = existing_indices[-1]
            df.at[idx, 'close'] = match_price
            df.at[idx, 'high'] = max(df.at[idx, 'high'], match_price)
            df.at[idx, 'low'] = min(df.at[idx, 'low'], match_price)
        else:
            last_ts = int(df.at[last_idx, 'time'])
            if last_ts < current_candle_ts:
                # Append nến mới
                new_row = {
                    'time': current_candle_ts,
                    'open': match_price,
                    'high': match_price,
                    'low': match_price,
                    'close': match_price,
                    'volume': 0,
                }
                for col in df.columns:
                    if col not in new_row:
                        new_row[col] = df.at[last_idx, col]
                df.loc[len(df)] = new_row
            
    except Exception as e:
        print(f"Error in patch_realtime_data: {e}")

def download_data(stock: Stock, vnindex_stock: Stock, trading_chart_type: CandleEnum, following_chart_type: CandleEnum):
    """
    Hàm wrapper giữ nguyên interface cũ nhưng sử dụng VNIndexManager để tối ưu.
    """
    vnindex_data_following = VNIndexManager.get_data(vnindex_stock, following_chart_type)
    vnindex_data_trading = VNIndexManager.get_data(vnindex_stock, trading_chart_type)

    stock_data_trading, stock_data_following = download_data_stock_only(stock, trading_chart_type, following_chart_type)

    return vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following

def download_sales_volume(symbol: str, max_retries: int = 3, timeout_per_request: int = 3):
    """
    Download sales volume data với timeout tổng cộng không quá 10s
    
    Args:
        symbol: Mã cổ phiếu
        max_retries: Số lần thử lại (default: 3)
        timeout_per_request: Timeout cho mỗi request (default: 3s)
    """
    board_id='MAIN'
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{symbol}"
    HEADERS = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    import time
    start_time = time.time()
    max_total_time = 10  # Tổng thời gian tối đa 10s
    
    for attempt in range(max_retries):
        # Kiểm tra tổng thời gian đã chạy
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_total_time:
            return None
            
        try:
            remaining_time = max_total_time - elapsed_time
            current_timeout = min(timeout_per_request, remaining_time)
            
            if current_timeout <= 0:
                return None
                
            response = requests.get(url, headers=HEADERS, timeout=current_timeout)
            response.raise_for_status()
            data_sales_volume = response.json()
            
            # Kiểm tra nếu là list và có phần tử đầu tiên
            if isinstance(data_sales_volume, list) and len(data_sales_volume) > 0:
                stock_data = data_sales_volume[0]  # Lấy phần tử đầu tiên trong danh sách

                data = {
                    'buyForeignQtty': stock_data.get('fBVol'),
                    'sellForeignQtty': stock_data.get('fSVolume'),
                    'ceil_price': stock_data.get('c'),
                    'floor_price': stock_data.get('f')
                }
                return data
            else:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed for {symbol}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None
    
    print(f"❌ Failed to download sales data for {symbol} after {max_retries} attempts in {time.time() - start_time:.2f}s")
    return None
