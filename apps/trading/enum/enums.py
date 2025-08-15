__all__ = []

from enum import Enum


class StatusPidEnum(Enum):
    BUY = 'Buying'
    SELL = 'Selling'
    FOLLOW = 'Following'


class BuyReasonType:
    pass


class SellReasonType:
    pass


class ChartType:
    Trading = 'trading'
    Following = 'following'
    Overview = 'overview'


class SellType:
    SellTrue = 'SellTrue'
    SellFalse = 'SellFalse'
    TakeProfit = 'TakeProfit'
    Stoploss = 'StopLoss'
