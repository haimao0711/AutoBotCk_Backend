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

def download_sales_volume(symbol: str):
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{symbol}"
    HEADERS = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Thiết lập session với retry
    session = requests.Session()
    retry = Retry(
        total=3,            # thử tối đa 3 lần
        backoff_factor=1,   # tăng thời gian chờ giữa các retry
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # raise lỗi nếu HTTP != 200

        data_sales_volume = response.json()

        if isinstance(data_sales_volume, list) and len(data_sales_volume) > 0:
            stock_data = data_sales_volume[0]

            data = {
                'buyForeignQtty': stock_data.get('fBVol'),
                'sellForeignQtty': stock_data.get('fSVolume'),
                'ceil_price': stock_data.get('c'),
                'floor_price': stock_data.get('f')
            }
            return data
        else:
            print(f"[Warning] Dữ liệu sales volume rỗng hoặc không hợp lệ cho symbol {symbol}")
            return None

    except requests.exceptions.Timeout:
        print(f"[Timeout] Không kết nối được API sales volume cho symbol {symbol}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[RequestException] Lỗi khi tải sales volume symbol {symbol}: {e}")
        return None

