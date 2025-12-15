__all__ = []

# ================================================================================================================================================================
# ================================================================================================================================================================
# =============================================================              ***BUY***                ============================================================
# ================================================================================================================================================================
# ================================================================================================================================================================


# ================================================================================================================================================================
# ================================================================================================================================================================
# VnIndex
# ================================================================================================================================================================
# ================================================================================================================================================================
BUY_PERMISSION = '''
        # Cấu hình dành cho mua chưa được thiết kế! ❌'''

NOT_VALID_TIME_TO_BUY = '''
        # Chưa đến thời gian bắt đầu mua! ❌'''


VNINDEX_CONFIG_MAX_VnIndex_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  VnIndex <=, cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**:  VnIndex >=, cấu hình ({previous}) *>=*hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_RSI_OBL_TO_BUY = '''
        # **ĐKbb:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        # **ĐKbb:**  StochRSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_MACD_OBL_TO_BUY = '''
        # **ĐKbb:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
        # **ĐKbb:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* tăng, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_USE_MACD_OBL_INCREASE= '''
        # **ĐKbb:**  MACD *(VNI)* tăng, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  SMA *(VNI)* tăng, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_USE_SMA_OBL_INCREASE= '''
        # **ĐKbb:**  SMA *(VNI)* tăng, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  Volume > VolumeMA *(VNI)*, Volume ({current}) >  VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_SUFFICIENT_CONDITION = '''              
        # **ĐK đủ:** Chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá hiện tại ({previous})'''

# ================================================================================================================================================================

VNINDEX_CONFIG_MAX_VnIndex_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* tăng, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  SMA *(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* tăng, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  Volume > VolumeMA *(VNI)*, Volume ({current}) > VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_NECESSARY_CONDITION = '''              
        # **ĐK cần:** Chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá hiện tại ({previous})'''


# ================================================================================================================================================================
# ================================================================================================================================================================
# Stock
# ================================================================================================================================================================
# ================================================================================================================================================================
STOCK_CONFIG_USE_RSI_OBL_TO_BUY = '''
        # **ĐKbb:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        # **ĐKbb:**  StochRSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_MACD_OBL_TO_BUY = '''
        # **ĐKbb:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
        # **ĐKbb:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_UP_OBL_TO_BUY = '''
        # **ĐKbb:** Mua chủ động *(CP)* >=, Hiện tại ({current}) *>=* Cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_FOREIGN_OBL_TO_BUY = '''
        # **ĐKbb:** Mua nước ngoài *(CP)* >=, Hiện tại ({current}) *>=* Cấu hình ({previous})'''
STOCK_CONFIG_USE_VOLUME_TRADE_OBL_TO_BUY = '''
        # **ĐKbb:** KL đã về *(CP)* >=, Hiện tại ({current}) *>=* Cấu hình ({previous})'''

STOCK_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* tăng, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  SMA *(CP)* tăng, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_USE_MACD_OBL_INCREASE = '''
        # **ĐKbb:**  MACD *(CP)* tăng, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_USE_SMA_OBL_INCREASE = '''
        # **ĐKbb:**  SMA *(CP)* tăng, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  Volume > VolumeMA *(CP)*, Volume ({current}) > VolumeMA ({previous})'''

# ================================================================================================================================================================

STOCK_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* <=, hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* ↘↗, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* tăng, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  SMA *(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* tăng, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        # **ĐK cần:**  Volume > VolumeMA *(CP)*, Volume ({current}) > VolumeMA ({previous})'''

# ================================================================================================================================================================
# ================================================================================================================================================================
# PRICE
# ================================================================================================================================================================
# ================================================================================================================================================================

GLOBAL_CONFIG_REQUEST_BUY_NOW_SUCCESS = '''
        # *Điều kiện mua chỉ sử dụng chart hành động* được kích hoạt ✅
                Thời gian đặt yêu cầu: {time_request_buy}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_REQUEST_BUY_NOW_FAILED = '''
        # *Điều kiện mua chỉ sử dụng chart hành độngc* không được kích hoạt ❌
                Thời gian đặt yêu cầu: {time_request_buy}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_BUY_PRICE_SUCCESS = '''
        # *Điều kiện mua theo Giá* được kích hoạt ✅
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

GLOBAL_CONFIG_BUY_PRICE_FAILED = '''
        # *Điều kiện mua theo Giá* không được kích hoạt ❌
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

ERROR_NOT_SETUP_BUY_TRADING_CONFIGURATION = '''
                # Chưa tiến hành cấu hình mua cho chart hành động'''

ERROR_NOT_SETUP_BUY_FOLLOWING_CONFIGURATION = '''
                # Chưa tiến hành cấu hình mua cho chart theo dõi'''

ERROR_NOT_SETUP_BUY_PERMISSION = '''
                # Chưa tiến hành cấp quyền mua cho tài khoản'''

# ================================================================================================================================================================
# ================================================================================================================================================================
# =============================================================              ***SELL***                ============================================================
# ================================================================================================================================================================
# ================================================================================================================================================================


# ================================================================================================================================================================
# ================================================================================================================================================================
# VnIndex
# ================================================================================================================================================================
# ================================================================================================================================================================
SELL_PERMISSION = '''
        # Cấu hình dành cho bán chưa được thiết kế! ❌'''

NOT_VALID_TIME_TO_SELL = '''
        # Chưa đến thời gian bắt đầu bán! ❌'''

VNINDEX_CONFIG_MAX_VnIndex_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**:  VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**:  VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(VNI)* giảm, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  SMA *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_SUFFICIENT_CONDITION = '''              
        # **ĐK đủ:** Giá chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''

# ================================================================================================================================================================

VNINDEX_CONFIG_MAX_VnIndex_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**:  VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**:  VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  SMA *(VNI)* giảm, mới: {current}, cũ: {previous}'''
VNINDEX_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* giảm, mới: {current}, cũ: {previous}'''

VNINDEX_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(VNI)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_NECESSARY_CONDITION = '''              
        # **ĐK cần:** Giá chạm cạnh dưới Bolinger *(VNI)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''


# ================================================================================================================================================================
# ================================================================================================================================================================
# Stock
# ================================================================================================================================================================
# ================================================================================================================================================================
STOCK_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  RSI *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  StochRSI *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  MACD *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  SMA *(CP)* giảm, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        # **ĐK đủ:**  His*(CP)* giảm, mới: {current}, cũ: {previous}'''

# ================================================================================================================================================================

STOCK_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* >=, hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* ↗↘, D2: {old_previous}, D1: {previous}, D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  RSI *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  StochRSI *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  MACD *(CP)* giảm, mới: {current}, cũ: {previous}'''

STOCK_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  SMA *(CP)* giảm, mới: {current}, cũ: {previous}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        # **ĐK cần:**  His*(CP)* giảm, mới: {current}, cũ: {previous}'''

# ================================================================================================================================================================
# ================================================================================================================================================================
# PRICE
# ================================================================================================================================================================
# ================================================================================================================================================================

GLOBAL_CONFIG_REQUEST_SELL_NOW_SUCCESS = '''
        # *Điều kiện bán chỉ sử dụng chart hành động* được kích hoạt ✅
                Thời gian đặt yêu cầu: {time_request_sell}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_REQUEST_SELL_NOW_FAILED = '''
        # *Điều kiện bán chỉ sử dụng chart hành độngc* không được kích hoạt ❌
                Thời gian đặt yêu cầu: {time_request_sell}
                Thời gian hiện tại {current_time}'''

GLOBAL_CONFIG_SELL_PRICE_SUCCESS = '''
        # *Điều kiện bán theo Giá* được kích hoạt ✅
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

GLOBAL_CONFIG_SELL_PRICE_FAILED = '''
        # *Điều kiện bán theo Giá* không được kích hoạt ❌
                Giá đặt: {set_price}
                Giá hiện tại {current_price}'''

ERROR_NOT_SETUP_SELL_TRADING_CONFIGURATION = '''
        # Chưa tiến hành cấu hình bán cho chart hành động'''

ERROR_NOT_SETUP_SELL_FOLLOWING_CONFIGURATION = '''
        # Chưa tiến hành cấu hình bán cho chart theo dõi'''

ERROR_NOT_SETUP_SELL_PERMISSION = '''
        # Chưa tiến hành cấp quyền bán cho tài khoản'''

# ================================================================================================================================================================
# ================================================================================================================================================================
# STOP LOSS & TAKE PROFIT
# ================================================================================================================================================================
# ================================================================================================================================================================
STOPLOSS_PRICE_SUCCESS = '''
        # *Điều kiện bán cắt lỗ* được kích hoạt ✅
                Giá cắt lỗ: {set_price}
                Giá hiện tại {current_price}'''

STOPLOSS_PRICE_FAILED = '''
        # *Điều kiện bán cắt lỗ* không được kích hoạt ❌
                Giá cắt lỗ: {set_price}
                Giá hiện tại {current_price}'''

TAKEPROFIT_PRICE_SUCCESS = '''
        # *Điều kiện bán chốt lãi* được kích hoạt ✅
                Giá chốt lãi: {set_price}
                Giá hiện tại {current_price}'''

TAKEPROFIT_PRICE_FAILED = '''
        # *Điều kiện bán chốt lãi* không được kích hoạt ❌
                Giá chốt lãi: {set_price}
                Giá hiện tại {current_price}'''
