from apps.stock.models import Stock
from apps.configuration.candle.enums import CandleEnum
from apps.stock.enums import DownloadStatusEnum
from apps.stock.services import DownloadService
from apps.trading.service.helper import adding_idicator
import requests
import pandas as pd
from datetime import datetime
import pytz

def patch_realtime_data(df, match_price, chart_type):
    if df is None or df.empty:
        return

    try:
        # timezone
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(tz)
        
        start_time = None
        
        if chart_type == CandleEnum.M1:
            start_time = now.replace(second=0, microsecond=0)
        elif chart_type == CandleEnum.M5:
            minute = (now.minute // 5) * 5
            start_time = now.replace(minute=minute, second=0, microsecond=0)
        elif chart_type == CandleEnum.M15:
            minute = (now.minute // 15) * 15
            start_time = now.replace(minute=minute, second=0, microsecond=0)
        elif chart_type == CandleEnum.H1:
            start_time = now.replace(minute=0, second=0, microsecond=0)
        elif chart_type == CandleEnum.D1:
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif chart_type == CandleEnum.W1:
            start_time = now - pd.Timedelta(days=now.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if start_time is None:
            return

        current_candle_ts = int(start_time.timestamp())
        
        last_idx = df.index[-1]
        last_ts = int(df.at[last_idx, 'time'])
        
        # --- Normalization Logic ---
        last_close = df.at[last_idx, 'close']
        if last_close > 0:
            ratio = match_price / last_close
            if ratio > 100:
                # Discrepancy detected (e.g. 30000 vs 30). Normalize match_price.
                match_price = match_price / 1000
            elif ratio < 0.01:
                # Inverse discrepancy (e.g. 30 vs 30000). Highly unlikely but safe to handle.
                match_price = match_price * 1000
        # ---------------------------
        
        if last_ts == current_candle_ts:
            df.at[last_idx, 'close'] = match_price
            df.at[last_idx, 'high'] = max(df.at[last_idx, 'high'], match_price)
            df.at[last_idx, 'low'] = min(df.at[last_idx, 'low'], match_price)
        elif last_ts < current_candle_ts:
            # Append
            new_row = {
                'time': current_candle_ts,
                'open': match_price,
                'high': match_price,
                'low': match_price,
                'close': match_price,
                'volume': 0,
                'id': df.at[last_idx, 'id'] if 'id' in df.columns else None
            }
            df.loc[len(df)] = new_row
            
    except Exception as e:
        print(f"Error in patch_realtime_data: {e}")

def download_data(stock: Stock, vnindex_stock: Stock, trading_chart_type: CandleEnum, following_chart_type: CandleEnum):
    try:
        vnindex_data_following = DownloadService.download_data_single(
            stock=vnindex_stock, chart_type=following_chart_type, download_status=DownloadStatusEnum.NEW.value)
        vnindex_data_trading = DownloadService.download_data_single(
            stock=vnindex_stock, chart_type=trading_chart_type, download_status=DownloadStatusEnum.NEW.value)
        
        # Patch realtime data for VNINDEX
        try:
            vnindex_info = DownloadService.get_stock_info(vnindex_stock.symbol, None)
            if vnindex_info and 'matchPrice' in vnindex_info:
                match_price = vnindex_info['matchPrice']
                patch_realtime_data(vnindex_data_following, match_price, following_chart_type)
                patch_realtime_data(vnindex_data_trading, match_price, trading_chart_type)
        except Exception as e:
            print(f"Error patching VNINDEX realtime data: {e}")

        adding_idicator(vnindex_data_following)
        adding_idicator(vnindex_data_trading)

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
    except Exception as error:
        print(str(error))
        return None, None, None, None

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
