from apps.stock.models import Stock
from apps.configuration.candle.enums import CandleEnum
from apps.stock.enums import DownloadStatusEnum
from apps.stock.services import DownloadService
from apps.trading.service.helper import adding_idicator
import requests

def download_data(stock: Stock, vnindex_stock: Stock, trading_chart_type: CandleEnum, following_chart_type: CandleEnum):
    try:
        vnindex_data_following = DownloadService.download_data_single(
            stock=vnindex_stock, chart_type=following_chart_type, download_status=DownloadStatusEnum.NEW.value)
        vnindex_data_trading = DownloadService.download_data_single(
            stock=vnindex_stock, chart_type=trading_chart_type, download_status=DownloadStatusEnum.NEW.value)
        
        # print(vnindex_data_following, vnindex_data_trading)
        
        adding_idicator(vnindex_data_following)
        adding_idicator(vnindex_data_trading)

        stock_data_following = DownloadService.download_data_single(
            stock=stock, chart_type=following_chart_type, download_status=DownloadStatusEnum.NEW.value)
        stock_data_trading = DownloadService.download_data_single(
            stock=stock, chart_type=trading_chart_type, download_status=DownloadStatusEnum.NEW.value)
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
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None
    
    print(f"❌ Failed to download sales data for {symbol} after {max_retries} attempts in {time.time() - start_time:.2f}s")
    return None
