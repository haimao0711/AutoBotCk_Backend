__all__ = []

BUY_PERMISSION = '''
        Cấu hình dành cho mua chưa được thiết kế! ❌'''

NOT_VALID_TIME_TO_BUY = '''
        Chưa đến thời gian bắt đầu mua! ❌'''


VNINDEX_CONFIG_MAX_VnIndex_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  VnIndex <=, cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**:  VnIndex >=, cấu hình ({previous}) *>=*hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_RSI_OBL_TO_BUY = '''
        **ĐKbb:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        **ĐKbb:**  Srsi *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_MACD_OBL_TO_BUY = '''
        **ĐKbb:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
        **ĐKbb:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* ↗, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_USE_MACD_OBL_INCREASE= '''
        **ĐKbb:**  MACD *(VNI)* ↗, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  SMA *(VNI)* ↗, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_USE_SMA_OBL_INCREASE= '''
        **ĐKbb:**  SMA *(VNI)* ↗, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Volume > VolumeMA *(VNI)*, Volume ({current}) >  VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_SUFFICIENT_CONDITION = '''              
        **ĐK đủ:** Chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá hiện tại ({previous})'''

VNINDEX_CONFIG_MAX_VnIndex_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  VnIndex <=, cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  VnIndex >=, cấu hình ({previous}) *>=* hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* ↗, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  SMA *(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* ↗, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  Volume > VolumeMA *(VNI)*, Volume ({current}) > VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_NECESSARY_CONDITION = '''              
        **ĐK cần:** Chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá hiện tại ({previous})'''


STOCK_CONFIG_USE_RSI_OBL_TO_BUY = '''
        **ĐKbb:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        **ĐKbb:**  Srsi *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_MACD_OBL_TO_BUY = '''
        **ĐKbb:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
        **ĐKbb:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_UP_OBL_TO_BUY = '''
        **ĐKbb:** Mua chủ động *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_FOREIGN_OBL_TO_BUY = '''
        **ĐKbb:** Mua NN *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''
STOCK_CONFIG_USE_VOLUME_TRADE_OBL_TO_BUY = '''
        **ĐKbb:** KL đã về *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* ↗, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  SMA *(CP)* ↗, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_USE_MACD_OBL_INCREASE = '''
        **ĐKbb:**  MACD *(CP)* ↗, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_USE_SMA_OBL_INCREASE = '''
        **ĐKbb:**  SMA *(CP)* ↗, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Volume > VolumeMA *(CP)*, Volume ({current}) > VolumeMA ({previous})'''


STOCK_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* ↗, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  SMA *(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* ↗, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        **ĐK cần:**  Volume > VolumeMA *(CP)*, Volume ({current}) > VolumeMA ({previous})'''


GLOBAL_CONFIG_REQUEST_BUY_NOW_SUCCESS = '''
        *Điều kiện mua chỉ sử dụng chart hành động* được kích hoạt ✅
                Thời gian đặt yêu cầu: {time_request_buy}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_REQUEST_BUY_NOW_FAILED = '''
        *Điều kiện mua chỉ sử dụng chart hành độngc* không được kích hoạt ❌
                Thời gian đặt yêu cầu: {time_request_buy}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_BUY_PRICE_SUCCESS = '''
        *Điều kiện mua theo Giá* được kích hoạt ✅
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

GLOBAL_CONFIG_BUY_PRICE_FAILED = '''
        *Điều kiện mua theo Giá* không được kích hoạt ❌
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

ERROR_NOT_SETUP_BUY_TRADING_CONFIGURATION = '''
                Chưa tiến hành cấu hình mua cho chart hành động'''

ERROR_NOT_SETUP_BUY_FOLLOWING_CONFIGURATION = '''
                Chưa tiến hành cấu hình mua cho chart theo dõi'''

ERROR_NOT_SETUP_BUY_PERMISSION = '''
                Chưa tiến hành cấp quyền mua cho tài khoản'''

PERMISSION = '''
        Cấu hình dành cho bán chưa được thiết kế! ❌'''

NOT_VALID_TIME_TO_SELL = '''
        Chưa đến thời gian bắt đầu bán! ❌'''

VNINDEX_CONFIG_MAX_VnIndex_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**:  VnIndex <=, cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**:  VnIndex >=, cấu hình ({previous}) *>=* hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(VNI)* ↘, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  SMA *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_SUFFICIENT_CONDITION = '''              
        **ĐK đủ:** Giá chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''

VNINDEX_CONFIG_MAX_VnIndex_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**:  VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**:  VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        - **ĐK cần:**  RSI *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        - **ĐK cần:**  Srsi *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  SMA *(VNI)* ↘, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* ↘, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_NECESSARY_CONDITION = '''              
        **ĐK cần:** Chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá hiện tại ({current})'''


STOCK_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  RSI *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  Srsi *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  MACD *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  SMA *(CP)* ↘, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        **ĐK đủ:**  His*(CP)* ↘, mới: {current}, cũ: {previous}'''


STOCK_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  RSI *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  Srsi *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  MACD *(CP)* ↘, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  SMA *(CP)* ↘, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        **ĐK cần:**  His*(CP)* ↘, mới: {current}, cũ: {previous}'''


GLOBAL_CONFIG_REQUEST_SELL_NOW_SUCCESS = '''
        *Điều kiện bán chỉ sử dụng chart hành động* được kích hoạt ✅
                Thời gian đặt yêu cầu: {time_request_sell}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_REQUEST_SELL_NOW_FAILED = '''
        *Điều kiện bán chỉ sử dụng chart hành độngc* không được kích hoạt ❌
                Thời gian đặt yêu cầu: {time_request_sell}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_SELL_PRICE_SUCCESS = '''
        *Điều kiện bán theo Giá* được kích hoạt ✅
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

GLOBAL_CONFIG_SELL_PRICE_FAILED = '''
        *Điều kiện bán theo Giá* không được kích hoạt ❌
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

ERROR_NOT_SETUP_SELL_TRADING_CONFIGURATION = '''
        Chưa tiến hành cấu hình bán cho chart hành động'''

ERROR_NOT_SETUP_SELL_FOLLOWING_CONFIGURATION = '''
        Chưa tiến hành cấu hình bán cho chart theo dõi'''

ERROR_NOT_SETUP_SELL_PERMISSION = '''
        Chưa tiến hành cấp quyền bán cho tài khoản'''

STOPLOSS_PRICE_SUCCESS = '''
        *Điều kiện bán cắt lỗ* được kích hoạt ✅
                Giá cắt lỗ: {set_price}
                Giá hiện tại {current_price}'''

STOPLOSS_PRICE_FAILED = '''
        *Điều kiện bán cắt lỗ* không được kích hoạt ❌
                Giá cắt lỗ: {set_price}
                Giá hiện tại {current_price}'''

TAKEPROFIT_PRICE_SUCCESS = '''
        *Điều kiện bán chốt lãi* được kích hoạt ✅
                Giá chốt lãi: {set_price}
                Giá hiện tại {current_price}'''

TAKEPROFIT_PRICE_FAILED = '''
        *Điều kiện bán chốt lãi* không được kích hoạt ❌
                Giá chốt lãi: {set_price}
                Giá hiện tại {current_price}'''
