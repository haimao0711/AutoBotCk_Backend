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
        # **Điều kiện đủ:** Giá trị VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:**: Giá trị VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''
VNINDEX_CONFIG_USE_RSI_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị RSI *(VnIndex)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''
VNINDEX_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* <=, StochRSI hiện tại ({current}) *<=* StochRSI cấu hình ({previous})'''
VNINDEX_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị StochRSI *(VnIndex)* <=, StochRSI hiện tại ({current}) *<=*  StochRSI cấu hình ({previous})'''
VNINDEX_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''
VNINDEX_CONFIG_USE_MACD_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị MACD *(VnIndex)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* đảo chiều tăng, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* tăng, RSI mới: {current}, RSI cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* đảo chiều tăng, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* tăng, StochRSI mới: {current}, StochRSI cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* đảo chiều tăng, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

VNINDEX_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* tăng, MACD mới: {current}, MACD cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(VnIndex)* đảo chiều tăng, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(VnIndex)* tăng, Histogram mới: {current}, Histogram cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Volume > VolumeMA *(VnIndex)*, Volume ({current}) > Giá trị VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_SUFFICIENT_CONDITION = '''              
        # **Điều kiện đủ:** Giá chạm cạnh dưới Bolinger *(VnIndex)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({previous})'''

# ================================================================================================================================================================

VNINDEX_CONFIG_MAX_VnIndex_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* <=, StochRSI hiện tại ({current}) *<=* StochRSI cấu hình ({previous})'''

VNINDEX_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* đảo chiều tăng, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

VNINDEX_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* tăng, RSI mới: {current}, RSI cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* đảo chiều tăng, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* đảo chiều tăng, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(VnIndex)* đảo chiều tăng, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* tăng, StochRSI mới: {current}, StochRSI cũ: {previous}'''

VNINDEX_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* tăng, MACD mới: {current}, MACD cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(VnIndex)* tăng, Histogram mới: {current}, Histogram cũ: {previous}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Volume > VolumeMA *(VnIndex)*, Volume ({current}) > VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_NECESSARY_CONDITION = '''              
        # **Điều kiện cần:** Giá chạm cạnh dưới Bolinger *(VnIndex)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({previous})'''


# ================================================================================================================================================================
# ================================================================================================================================================================
# Stock
# ================================================================================================================================================================
# ================================================================================================================================================================
STOCK_CONFIG_USE_RSI_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị RSI *(Stock)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''

STOCK_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị StochRSI *(Stock)* <=, StochRSI hiện tại ({current}) *<=* StochRSI cấu hình ({previous})'''

STOCK_CONFIG_USE_MACD_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị MACD *(Stock)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_UP_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị Mua chủ động *(Stock)* >=, Mua chủ động hiện tại ({current}) *>=* Mua chủ động cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_FOREIGN_OBL_TO_BUY = '''
        # **Điều kiện bắt buộc:** Giá trị Mua nước ngoài *(Stock)* >=, Mua nước ngoài hiện tại ({current}) *>=* Mua nước ngoài cấu hình ({previous})'''


STOCK_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* <=, StochRSI hiện tại ({current}) *<=* StochRSI cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* đảo chiều tăng, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* đảo chiều tăng, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* đảo chiều tăng, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(Stock)* đảo chiều tăng, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* tăng, RSI mới: {current}, RSI cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* tăng, StochRSI mới: {current}, StochRSI cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* tăng, MACD mới: {current}, MACD cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(Stock)* tăng, Histogram mới: {current}, Histogram cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Volume > VolumeMA *(Stock)*, Volume ({current}) > VolumeMA ({previous})'''

# ================================================================================================================================================================

STOCK_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* <=, RSI hiện tại ({current}) *<=* RSI cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* <=, StochRSI hiện tại ({current}) *<=* StochRSI cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* <=, MACD hiện tại ({current}) *<=* MACD cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* đảo chiều tăng, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* đảo chiều tăng, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* đảo chiều tăng, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(Stock)* đảo chiều tăng, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

STOCK_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* tăng, RSI mới: {current}, RSI cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* tăng, StochRSI mới: {current}, StochRSI cũ: {previous}'''

STOCK_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* tăng, MACD mới: {current}, MACD cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(Stock)* tăng, Histogram mới: {current}, Histogram cũ: {previous}'''

STOCK_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Volume > VolumeMA *(Stock)*, Volume ({current}) > VolumeMA ({previous})'''

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
        # **Điều kiện đủ:**: Giá trị VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:**: Giá trị VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* >=, RSI hiện tại ({current}) *>=* RSI cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* >=, StochRSI hiện tại ({current}) *>=* StochRSI cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* >=, MACD hiện tại ({current}) *>=* MACD cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* đảo chiều giảm, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

VNINDEX_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(VnIndex)* giảm, RSI mới: {current}, RSI cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* đảo chiều giảm, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(VnIndex)* giảm, StochRSI mới: {current}, StochRSI cũ: {previous}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* đảo chiều giảm, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

VNINDEX_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(VnIndex)* giảm, MACD mới: {current}, MACD cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(VnIndex)* đảo chiều giảm, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(VnIndex)* giảm, Histogram mới: {current}, Histogram cũ: {previous}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_SUFFICIENT_CONDITION = '''              
        # **Điều kiện đủ:** Giá chạm cạnh dưới Bolinger *(VnIndex)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''

# ================================================================================================================================================================

VNINDEX_CONFIG_MAX_VnIndex_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:**: Giá trị VnIndex <=, VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:**: Giá trị VnIndex >=, VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* >=, RSI hiện tại ({current}) *>=* RSI cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* >=, StochRSI hiện tại ({current}) *>=* StochRSI cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* >=, MACD hiện tại ({current}) *>=* MACD cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* giảm, RSI mới: {current}, RSI cũ: {previous}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* giảm, StochRSI mới: {current}, StochRSI cũ: {previous}'''

VNINDEX_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* giảm,  MACD mới: {current}, MACD cũ: {previous}'''

VNINDEX_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(VnIndex)* giảm, Histogram mới: {current}, Histogram cũ: {previous}'''

VNINDEX_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(VnIndex)* đảo chiều giảm, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(VnIndex)* đảo chiều giảm, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(VnIndex)* đảo chiều giảm, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(VnIndex)* đảo chiều giảm, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_NECESSARY_CONDITION = '''              
        # **Điều kiện cần:** Giá chạm cạnh dưới Bolinger *(VnIndex)*, Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''


# ================================================================================================================================================================
# ================================================================================================================================================================
# Stock
# ================================================================================================================================================================
# ================================================================================================================================================================
STOCK_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* >=, RSI hiện tại ({current}) *>=* RSI cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* >=, StochRSI hiện tại ({current}) *>=* StochRSI cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* >=, MACD hiện tại ({current}) *>=* MACD cấu hình ({previous}) '''

STOCK_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* đảo chiều giảm, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* đảo chiều giảm, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* đảo chiều giảm, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(Stock)* đảo chiều giảm, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị RSI *(Stock)* giảm, RSI mới: {current}, RSI cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị StochRSI *(Stock)* giảm, StochRSI mới: {current}, StochRSI cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị MACD *(Stock)* giảm, MACD mới: {current}, MACD cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
        # **Điều kiện đủ:** Giá trị Histogram *(Stock)* giảm, Histogram mới: {current}, Histogram cũ: {previous}'''

# ================================================================================================================================================================

STOCK_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* >=, RSI hiện tại ({current}) *>=* RSI cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* >=, StochRSI hiện tại ({current}) *>=* StochRSI cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* >=, MACD hiện tại ({current}) *>=* MACD cấu hình ({previous}) '''
STOCK_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* đảo chiều giảm, RSI D2: {old_previous}, RSI D1: {previous}, RSI D0: {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* đảo chiều giảm, StochRSI D2: {old_previous}, StochRSI D1: {previous}, StochRSI D0: {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* đảo chiều giảm, MACD D2: {old_previous}, MACD D1: {previous}, MACD D0: {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(Stock)* đảo chiều giảm, Histogram D2: {old_previous}, Histogram D1: {previous}, Histogram D0: {current}'''


STOCK_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị RSI *(Stock)* giảm, RSI mới: {current}, RSI cũ: {previous}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị StochRSI *(Stock)* giảm, StochRSI mới: {current}, StochRSI cũ: {previous}'''

STOCK_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị MACD *(Stock)* giảm, MACD mới: {current}, MACD cũ: {previous}'''

STOCK_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
        # **Điều kiện cần:** Giá trị Histogram *(Stock)* giảm, Histogram mới: {current}, Histogram cũ: {previous}'''

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
