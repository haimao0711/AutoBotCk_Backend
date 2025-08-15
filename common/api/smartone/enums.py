from enum import Enum


class ResponseAPISmartOneEnum(Enum):
    SUCCESS = 1
    INVALID_SESSION_CODE = -1
    INVALID_STOCK_NAME_CODE = -8038
    INVALID_STEP_PRICE_CODE = -8029
    INVALID_RANGE_PRICE_CODE = -6035
    INVALID_REFERANCE_ID_CODE = -6018
    NOT_CHANGE_CANCEL_CODE = -6015
    INVALID_TIME_TRADING_CODE = -8025
    INVALID_CANCEL_ORDER_CODE = -8017


class StatusOrderEnum(Enum):
    MATCHING_ALL = 2
    MATCHING_PART = 1
    FOLLOWING = 0
    UPDATE = -1
    CANCEL = -2


class SideOrderEnum(Enum):
    BUY = 1
    SELL = 0
    
class StatusTransactionEnum(Enum):
    MATCH = 1
    CANCEL = 2
    UNKNOWN = 3
