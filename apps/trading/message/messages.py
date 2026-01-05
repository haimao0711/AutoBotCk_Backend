__all__ = []

BUY_PERMISSION = '''
        Cấu hình dành cho mua chưa được thiết kế! ❌'''

NOT_VALID_TIME_TO_BUY = '''
        Chưa đến thời gian bắt đầu mua! ❌'''


VNINDEX_CONFIG_MAX_VnIndex_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(VnIndex <=): hiện tại ({current}) *<=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(VnIndex >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_RSI_OBL_TO_BUY = '''
**ĐkBb**(RSI *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
**ĐkBb**(Srsi *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_MACD_OBL_TO_BUY = '''
**ĐkBb**(MACD *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
VNINDEX_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
**ĐkBb**(His*(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* ↗): {previous} ↗ {current}'''
VNINDEX_CONFIG_USE_MACD_OBL_INCREASE= '''
**ĐkBb**(MACD *(VNI)* ↗): {previous} ↗ {current}'''
VNINDEX_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(SMA *(VNI)* ↗): {previous} ↗ {current}'''
VNINDEX_CONFIG_USE_SMA_OBL_INCREASE= '''
**ĐkBb**(SMA *(VNI)* ↗): {previous} ↗ {current}'''
VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Volume > VolumeMA *(VNI)*): Volume ({current}) >  VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_SUFFICIENT_CONDITION = '''              
**ĐkĐủ**(Chạm cạnh dưới Bolinger *(VNI)*): Bolinger ({previous}) >= Giá hiện tại ({previous})'''

VNINDEX_CONFIG_MAX_VnIndex_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(VnIndex <=): cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(VnIndex >=): cấu hình ({previous}) *>=* hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

VNINDEX_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

VNINDEX_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* ↗): {previous} ↗ {current}'''
VNINDEX_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(SMA *(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* ↗): {previous} ↗ {current}'''

VNINDEX_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(Volume > VolumeMA *(VNI)*): Volume ({current}) > VolumeMA ({previous})'''

VNINDEX_CONFIG_BOLINGER_TO_BUY_NECESSARY_CONDITION = '''              
**ĐkCần**(Chạm cạnh dưới Bolinger *(VNI)*): Bolinger ({previous}) >= Giá hiện tại ({previous})'''


STOCK_CONFIG_USE_RSI_OBL_TO_BUY = '''
**ĐkBb**(RSI *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_STOCH_RSI_OBL_TO_BUY = '''
**ĐkBb**(Srsi *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_USE_MACD_OBL_TO_BUY = '''
**ĐkBb**(MACD *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_HISTOGRAM_OBL_TO_BUY = '''
**ĐkBb**(His*(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_UP_OBL_TO_BUY = '''
**ĐkBb**(Mua chủ động *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''
STOCK_CONFIG_USE_BUY_FOREIGN_OBL_TO_BUY = '''
**ĐkBb**(Mua NN *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''
STOCK_CONFIG_USE_VOLUME_TRADE_OBL_TO_BUY = '''
**ĐkBb**(KL đã về *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_RSI_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_MACD_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* ↗): {previous} ↗ {current}'''
STOCK_CONFIG_SMA_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(SMA *(CP)* ↗): {previous} ↗ {current}'''
STOCK_CONFIG_USE_MACD_OBL_INCREASE = '''
**ĐkBb**(MACD *(CP)* ↗): {previous} ↗ {current}'''
STOCK_CONFIG_USE_SMA_OBL_INCREASE = '''
**ĐkBb**(SMA *(CP)* ↗): {previous} ↗ {current}'''
STOCK_CONFIG_HISTOGRAM_INCREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_VOLUME_TO_BUY_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Volume > VolumeMA *(CP)*): Volume ({current}) > VolumeMA ({previous})'''


STOCK_CONFIG_RSI_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_MACD_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_HISTOGRAM_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* <=): hiện tại ({current}) *<=* cấu hình ({previous})'''

STOCK_CONFIG_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_MACD_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* ↘↗): {old_previous} ↘ {previous} ↗ {current}'''

STOCK_CONFIG_RSI_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_STOCH_RSI_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_MACD_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* ↗): {previous} ↗ {current}'''
STOCK_CONFIG_SMA_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(SMA *(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_HISTOGRAM_INCREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* ↗): {previous} ↗ {current}'''

STOCK_CONFIG_VOLUME_TO_BUY_NECESSARY_CONDITION = '''
**ĐkCần**(Volume > VolumeMA *(CP)*): Volume ({current}) > VolumeMA ({previous})'''


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
**ĐkĐủ**(VnIndex <=): cấu hình ({previous}) *<=* hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(VnIndex >=): cấu hình ({previous}) *>=* hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(VNI)* ↘): {previous} ↘ {current}'''
VNINDEX_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(SMA *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_SUFFICIENT_CONDITION = '''              
**ĐkĐủ**(Giá chạm cạnh dưới Bolinger *(VNI)*): Bolinger ({previous}) >= Giá cổ phiếu hiện tại ({current})'''

VNINDEX_CONFIG_MAX_VnIndex_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(VnIndex <=): VnIndex cấu hình ({previous}) *<=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_MIN_VnIndex_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(VnIndex >=): VnIndex cấu hình ({previous}) *>=* VnIndex hiện tại ({current}) '''

VNINDEX_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''

VNINDEX_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''
VNINDEX_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

VNINDEX_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(SMA *(VNI)* ↘): {previous} ↘ {current}'''
VNINDEX_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* ↘): {previous} ↘ {current}'''

VNINDEX_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(VNI)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

VNINDEX_CONFIG_BOLINGER_TO_SELL_NECESSARY_CONDITION = '''              
**ĐkCần**(Giá chạm cạnh dưới Bolinger *(VNI)*): Bolinger ({previous}) >= Giá hiện tại ({current})'''


STOCK_CONFIG_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_HISTOGRAM_TO_SELL_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''


STOCK_CONFIG_RSI_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(RSI *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(Srsi *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_MACD_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(MACD *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_SMA_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(SMA *(CP)* ↘): {previous} ↘ {current}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_SUFFICIENT_CONDITION = '''
**ĐkĐủ**(His*(CP)* ↘): {previous} ↘ {current}'''


STOCK_CONFIG_RSI_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous})'''

STOCK_CONFIG_STOCH_RSI_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''

STOCK_CONFIG_MACD_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_HISTOGRAM_TO_SELL_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* >=): hiện tại ({current}) *>=* cấu hình ({previous}) '''
STOCK_CONFIG_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_STOCH_RSI_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_MACD_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''

STOCK_CONFIG_HISTOGRAM_REVERSED_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* ↗↘): {old_previous} ↗ {previous} ↘ {current}'''


STOCK_CONFIG_RSI_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(RSI *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_STOCH_RSI_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(Srsi *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_MACD_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(MACD *(CP)* ↘): {previous} ↘ {current}'''

STOCK_CONFIG_SMA_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(SMA *(CP)* ↘): {previous} ↘ {current}'''
STOCK_CONFIG_HISTOGRAM_DECREASE_NECESSARY_CONDITION = '''
**ĐkCần**(His*(CP)* ↘): {previous} ↘ {current}'''


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
