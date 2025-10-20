from common.errors.messages import ErrorMessages

from apps.configuration.candle.enums import CandleEnum

from django.db import models

from apps.trading.enum.enums import ChartType

from .serializers import StockSerializer
from .models import Stock, StockW1, StockD1, StockH1, StockM15, StockM5, StockM1
from .enums import (DataParamsTimeEnums, DayOfWeekEnum, DownloadCoefficientExistEnum,
                    DownloadCoefficientMondayExistEnum, DownloadCoefficientMondayNewEnum,
                    DownloadCoefficientNewEnum, DownloadCoefficientWeekendNewEnum, DownloadCoefficientWeekendExistEnum, DownloadStatusEnum,
                    SecondTimeEnums)
from django.db.models import OuterRef, Subquery, F
from datetime import datetime
import pytz
import concurrent.futures
import requests
import pandas as pd


class DownloadService:

    @staticmethod
    def _convert_chart_type_to_data(chart_type, download_status):
        current_time = datetime.now()
        current_day = current_time.weekday()
        if current_day == DayOfWeekEnum.MONDAY.value and download_status == DownloadStatusEnum.NEW.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayNewEnum.M1.value, DataParamsTimeEnums.M1.value
            # DownloadCoefficientMondayNewEnum = DownloadCoefficientMondayEnum

        elif current_day == DayOfWeekEnum.MONDAY.value and download_status == DownloadStatusEnum.EXIST.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_WEEK.value * DownloadCoefficientMondayExistEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientMondayExistEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_HOUR.value * DownloadCoefficientMondayExistEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_QUARTER_HOUR.value * DownloadCoefficientMondayExistEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_FIVE_MINUTES.value * DownloadCoefficientMondayExistEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_MINUTE.value * DownloadCoefficientMondayExistEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_MINUTE.value * DownloadCoefficientMondayExistEnum.M1.value, DataParamsTimeEnums.M1.value

        elif (current_day == DayOfWeekEnum.SATURDAY.value or current_day == DayOfWeekEnum.SUNDAY.value) and download_status == DownloadStatusEnum.NEW.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendNewEnum.M1.value, DataParamsTimeEnums.M1.value

        elif (current_day == DayOfWeekEnum.SATURDAY.value or current_day == DayOfWeekEnum.SUNDAY.value) and download_status == DownloadStatusEnum.EXIST.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_WEEK.value * DownloadCoefficientWeekendExistEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientWeekendExistEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_HOUR.value * DownloadCoefficientWeekendExistEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_QUARTER_HOUR.value * DownloadCoefficientWeekendExistEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_FIVE_MINUTES.value * DownloadCoefficientWeekendExistEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_MINUTES.value * DownloadCoefficientWeekendExistEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_MINUTES.value * DownloadCoefficientWeekendExistEnum.M1.value, DataParamsTimeEnums.M1.value

        elif current_day != DayOfWeekEnum.MONDAY.value and download_status == DownloadStatusEnum.NEW.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientNewEnum.M1.value, DataParamsTimeEnums.M1.value

        elif current_day != DayOfWeekEnum.MONDAY.value and download_status == DownloadStatusEnum.EXIST.value:
            match chart_type:
                case CandleEnum.W1:
                    return SecondTimeEnums.SECOND_IN_WEEK.value * DownloadCoefficientExistEnum.W1.value, DataParamsTimeEnums.W1.value
                case CandleEnum.D1:
                    return SecondTimeEnums.SECOND_IN_DAY.value * DownloadCoefficientExistEnum.D1.value, DataParamsTimeEnums.D1.value
                case CandleEnum.H1:
                    return SecondTimeEnums.SECOND_IN_HOUR.value * DownloadCoefficientExistEnum.H1.value, DataParamsTimeEnums.H1.value
                case CandleEnum.M15:
                    return SecondTimeEnums.SECOND_IN_QUARTER_HOUR.value * DownloadCoefficientExistEnum.M15.value, DataParamsTimeEnums.M15.value
                case CandleEnum.M5:
                    return SecondTimeEnums.SECOND_IN_FIVE_MINUTES.value * DownloadCoefficientExistEnum.M5.value, DataParamsTimeEnums.M5.value
                case CandleEnum.M1:
                    return SecondTimeEnums.SECOND_IN_MINUTE.value * DownloadCoefficientExistEnum.M1.value, DataParamsTimeEnums.M1.value
                case _:
                    return SecondTimeEnums.SECOND_IN_MINUTE.value * DownloadCoefficientExistEnum.M1.value, DataParamsTimeEnums.M1.value

        else:
            print('đã vào else')
            return 0, DataParamsTimeEnums.D1.value

    @staticmethod
    def download_data_weekly(stock, download_status):
        from datetime import datetime
        import pandas as pd
        import requests
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry

        API_VNDIRECT = "https://dchart-api.vndirect.com.vn/dchart/history"
        HEADERS = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        current_timestamp = datetime.now().timestamp()

        # Lấy khoảng thời gian cần tải
        time_to_download, _ = DownloadService._convert_chart_type_to_data(
            chart_type=CandleEnum.W1,
            download_status=download_status
        )

        params = {
            "resolution": '1D',  # dữ liệu ngày
            "symbol": stock.symbol,
            "from": int(current_timestamp - time_to_download),
            "to": int(current_timestamp),
        }

        # Thiết lập session với retry
        session = requests.Session()
        retry = Retry(
            total=3,            # retry tối đa 3 lần
            backoff_factor=1,   # mỗi lần retry tăng thời gian chờ
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            res = session.get(API_VNDIRECT, params=params, headers=HEADERS, timeout=10)
            res.raise_for_status()

            if not res.content:
                print(f"[Warning] API trả dữ liệu rỗng cho symbol {stock.symbol}")
                return pd.DataFrame()

            try:
                json_data = res.json()
                json_data.pop('s', None)

                # Tạo DataFrame ngày
                df = pd.DataFrame({
                    'time': pd.to_datetime(json_data['t'], unit='s'),
                    'open': json_data['o'],
                    'high': json_data['h'],
                    'low': json_data['l'],
                    'close': json_data['c'],
                    'volume': json_data['v'],
                })

                df.set_index('time', inplace=True)

                # Resample tuần
                weekly_df = df.resample('W').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                }).dropna()

                weekly_df = weekly_df.reset_index()
                weekly_df['time'] = weekly_df['time'].astype('int64') // 10**9
                weekly_df['id'] = stock.id

                return weekly_df

            except Exception as e:
                print(f"[Error] Xử lý dữ liệu tuần cho symbol {stock.symbol} thất bại: {e}")
                return pd.DataFrame()

        except requests.exceptions.Timeout:
            print(f"[Timeout] Không kết nối được API cho symbol {stock.symbol}")
            return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            print(f"[RequestException] Lỗi khi download dữ liệu tuần symbol {stock.symbol}: {e}")
            return pd.DataFrame()



    @staticmethod
    def download_data(stocks, chart_type, download_status):
        from datetime import datetime
        import json
        import requests
        import time

        API_VNDIRECT = "https://dchart-api.vndirect.com.vn/dchart/history"

        HEADERS = {'content-type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Mozilla'}
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_timestamp = datetime.now(vietnam_tz).timestamp()

        time_to_download, resolution = DownloadService._convert_chart_type_to_data(
            chart_type=chart_type, download_status=download_status)
        
        data_download = []

        for stock in stocks:
            time_to_download, resolution = DownloadService._convert_chart_type_to_data(
                chart_type=chart_type, download_status=download_status)
            
            params = {
                "resolution": resolution,
                "symbol": stock.symbol,
                "from": int((current_timestamp - time_to_download)),
                "to": int(current_timestamp),
            }

            res = requests.get(API_VNDIRECT, params=params, headers=HEADERS)
            if res.status_code == 200:
                try:
                    data = res.content
                    decoded_data = data.decode('utf-8')
                    if not decoded_data.strip():
                        print(f"Empty response for {stock.symbol}")
                        continue
                    json_data = json.loads(decoded_data)
                    json_data.pop('s')

                    key_mapping = {'t': 'time', 'c': 'close',
                                   'o': 'open', 'l': 'low', 'h': 'high', 'v': 'volume'}

                    renamed_data = [{key_mapping.get(key, key): value[i] for key, value in json_data.items(
                    )} for i in range(len(json_data['t']))]

                    for item in renamed_data:
                        item['id'] = stock.id

                    data_download = data_download + renamed_data

                except ValueError as e:
                    print(f"Error down d1,m5,... khi status là 200: {e}")
                    continue

            else:
                print(f"Error down d1,m5,... khi status là 200: {res.status_code}")
                continue
        return data_download

    @staticmethod
    def download_data_single(stock, chart_type, download_status):
        from datetime import datetime
        import json
        import pandas as pd
        import requests
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry
        import time

        API_VNDIRECT = "https://dchart-api.vndirect.com.vn/dchart/history"
        HEADERS = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        current_timestamp = datetime.now().timestamp()
        data_download = []

        # Nếu chart_type là weekly, gọi hàm riêng
        if chart_type == CandleEnum.W1:
            res_week = DownloadService.download_data_weekly(stock, download_status)
            return res_week

        # Chuyển chart_type sang resolution và khoảng thời gian
        time_to_download, resolution = DownloadService._convert_chart_type_to_data(
            chart_type=chart_type, download_status=download_status)

        params = {
            "resolution": resolution,
            "symbol": stock.symbol,
            "from": int((current_timestamp - time_to_download)),
            "to": int(current_timestamp),
        }

        # Thiết lập session với retry
        session = requests.Session()
        retry = Retry(
            total=3,  # retry tối đa 3 lần
            backoff_factor=1,  # mỗi lần retry tăng thời gian chờ
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            res = session.get(API_VNDIRECT, params=params, headers=HEADERS, timeout=10)
            res.raise_for_status()  # raise lỗi nếu HTTP != 200

            if res.content:
                try:
                    json_data = res.json()
                    # Xoá key 's' nếu có
                    json_data.pop('s', None)

                    key_mapping = {'t': 'time', 'c': 'close', 'o': 'open', 'l': 'low', 'h': 'high', 'v': 'volume'}
                    renamed_data = [
                        {key_mapping.get(k, k): v[i] for k, v in json_data.items()}
                        for i in range(len(json_data['t']))
                    ]

                    # Thêm stock.id
                    for item in renamed_data:
                        item['id'] = stock.id

                    data_download += renamed_data

                except (ValueError, KeyError) as e:
                    print(f"[Error] Download data symbol {stock.symbol}, parse JSON failed: {e}")
                    return pd.DataFrame()

            else:
                print(f"[Warning] API trả dữ liệu rỗng cho symbol {stock.symbol}")
                return pd.DataFrame()

        except requests.exceptions.Timeout:
            print(f"[Timeout] Không kết nối được API cho symbol {stock.symbol}")
            return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            print(f"[RequestException] Lỗi khi download data symbol {stock.symbol}: {e}")
            return pd.DataFrame()

        return pd.DataFrame(data_download)

    @staticmethod
    def get_stock_info(stock_code, asp_net_session): 

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        api_url = "https://api-finfo.vndirect.com.vn/v4/effective_secinfo"
        params = {"q": f"code:{stock_code}"}

        try:
            response = requests.get(api_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"API trả về lỗi với mã trạng thái: {response.status_code}")
                print("Header phản hồi:", response.headers)
                print('Nội dung phản hồi:', response.text)
                return {}
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                stock_data = data["data"][0]
                result = {
                    "basicPrice": stock_data.get("basicPrice"),
                    "ceilPrice": stock_data.get("ceilPrice"),
                    "floorPrice": stock_data.get("floorPrice"),
                    "matchPrice": stock_data.get("matchPrice"),
                    "tradingDate": stock_data.get("tradingDate"),
                }
                return result
            else:
                print(f"Không tìm thấy thông tin cho mã cổ phiếu: {stock_code}")
                return {}

        except Exception as e:
            print(f"Lỗi xảy ra khi gọi API: {e}")
            return {}


class StockService:

    @staticmethod
    def get_stock_by_id(stock_id):
        try:
            stock = Stock.objects.get(id=stock_id)
            return stock
        except Stock.DoesNotExist:
            raise ValueError(ErrorMessages.STOCK_DOES_NOT_EXIST)

    @staticmethod
    def get_stocks_by_ids(stock_ids):
        try:
            stocks = Stock.objects.filter(id__in=stock_ids)
            return stocks
        except Stock.DoesNotExist:
            raise ValueError(ErrorMessages.STOCK_DOES_NOT_EXIST)

    @staticmethod
    def get_stock_by_symbol(stock_symbol):
        try:
            stock = Stock.objects.get(symbol=stock_symbol)
            return stock
        except Stock.DoesNotExist:
            raise ValueError(ErrorMessages.STOCK_DOES_NOT_EXIST)

    @staticmethod
    def get_stock_models_from_candle(candle_type):
        match candle_type:
            case CandleEnum.D1:
                return StockD1
            case CandleEnum.H1:
                return StockH1
            case CandleEnum.M15:
                return StockM15
            case CandleEnum.M5:
                return StockM5
            case CandleEnum.M1:
                return StockM1
            case _:
                return StockM1

    @staticmethod
    def get_last_stock_chart_item_by_time(StockModel: models.Model, stock_id):
        stock_data = StockModel.objects.filter(
            stock=stock_id).order_by('-time').first()
        return stock_data



    @staticmethod
    def get_last_stock_chart_items_by_time_bulk(StockModel: models.Model, stock_ids: list[int]):
        """
        Lấy dữ liệu cuối cùng cho nhiều stock_id cùng lúc.
        """
        stock_data = (
            StockModel.objects.filter(stock__in=stock_ids)
            .order_by('stock', '-time')  # Sắp xếp theo stock và thời gian giảm dần
            .distinct('stock')  # Giữ lại bản ghi mới nhất cho mỗi stock
        )
        return [{'id': item.stock.id, 'low': item.low, 'high': item.high, 'close': item.close} for item in stock_data]



    @staticmethod
    def get_second_last_stock_chart_item_by_time(StockModel: models.Model, stock_id) -> models.Model | None:
        queryset = StockModel.objects.filter(stock=stock_id).order_by('-time')

        if queryset.count() >= 2:
            second_last_item = queryset[1]
            return second_last_item
        else:
            return None

    @staticmethod
    def get_second_last_stock_chart_items_by_time_bulk(StockModel: models.Model, stock_ids: list[int]):
        """
        Lấy dữ liệu thứ hai mới nhất cho nhiều stock_id cùng lúc.
        """
        stock_data = (
            StockModel.objects.filter(stock__in=stock_ids)
            .order_by('stock', '-time')  # Sắp xếp theo stock và thời gian giảm dần
        )

        # Dữ liệu sẽ được gom nhóm theo stock_id
        result = {}
        for stock_id in stock_ids:
            items = stock_data.filter(stock=stock_id)[:2]  # Lấy tối đa 2 bản ghi
            if len(items) == 2:
                result[stock_id] = {
                    'id': items[1].stock.id,
                    'low': items[1].low,
                    'high': items[1].high,
                    'close': items[1].close,
                }
        return result.values()



    @staticmethod
    def get_yesterday_volume(stock: Stock | None):
        if stock is None:
            return 0

        data = DownloadService.download_data_single(
            stock=stock, chart_type=CandleEnum.D1, download_status=DownloadStatusEnum.NEW.value)
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vietnam_tz)

        start_time = now.replace(hour=14, minute=45, second=0, microsecond=0)
        end_time = now.replace(
            hour=23, minute=59, second=59, microsecond=999999)

        if start_time <= now <= end_time:
            return data.iloc[-1]['volume']
        else:
            return data.iloc[-2]['volume']


    @staticmethod
    def get_stocks_for_configuration():
        try:
            stocks = Stock.objects.filter(
                configuration__isnull=False).distinct()

            return stocks

        except Exception as e:
            print(f"Error fetching stocks for configuration: {e}")
            return []

    @staticmethod
    def update_or_create_stock(StockModel: models.Model, data):
    # Lấy thông tin cổ phiếu từ Stock model dựa trên stock_id
      stock = Stock.objects.get(id=data['id'])
    
    # Tạo bản ghi mới với thông tin cổ phiếu tại thời điểm hiện tại
      new_stock_data = StockModel.objects.create(
        time=data['time'],
        stock=stock,
        close=data['close'],
        open=data['open'],
        low=data['low'],
        high=data['high'],
        volume=data['volume']
      )
    
      return new_stock_data
   
    @staticmethod
    def create_stock(StockModel: models.Model, data):
        stock = Stock.objects.get(id=data['id'])
        new_stock_data = StockModel.objects.create(
            time=data['time'],
            stock=stock,
            close=data['close'],
            open=data['open'],
            low=data['low'],
            high=data['high'],
            volume=data['volume']
        )
        return new_stock_data

    @staticmethod
    def create_stocks(chart_type, stocks):
        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=chart_type, download_status=DownloadStatusEnum.NEW.value)
        for stock_data in stocks_download:
            stock_model = StockService.get_stock_models_from_candle(chart_type)
            StockService.update_or_create_stock(stock_model, stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_w1():
        stocks = StockService.get_stocks_for_configuration()

        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.W1, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockW1, data=stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_d1():
        stocks = StockService.get_stocks_for_configuration()

        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.D1, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockD1, data=stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_h1():
        stocks = StockService.get_stocks_for_configuration()

        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.H1, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockH1, data=stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_m15():
        stocks = StockService.get_stocks_for_configuration()
        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.M15, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockM15, data=stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_m5():
        stocks = StockService.get_stocks_for_configuration()

        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.M5, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockM5, data=stock_data)

    @staticmethod
    def download_and_imported_data_to_datbase_chart_m1():
        stocks = StockService.get_stocks_for_configuration()

        stocks_download = DownloadService.download_data(
            stocks=stocks, chart_type=CandleEnum.M1, download_status=DownloadStatusEnum.EXIST.value)

        for stock_data in stocks_download:
            _ = StockService.update_or_create_stock(
                StockModel=StockM1, data=stock_data)

    @staticmethod
    def download_imported_new_data_to_database_chart(stock_ids):
        stocks = StockService.get_stocks_by_ids(stock_ids=stock_ids)
        chart_types = [CandleEnum.D1, CandleEnum.H1,
                       CandleEnum.M15, CandleEnum.M5, CandleEnum.M1]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                StockService.create_stocks, chart_type, stocks) for chart_type in chart_types]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")

