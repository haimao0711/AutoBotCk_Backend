from django.db import models

from .enums import CandleEnum

import common.table_names as table

class Candle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    candle = models.CharField(max_length=50, choices=[(candle.name, candle.value) for candle in CandleEnum])
    candle_second = models.CharField(max_length=50, default=CandleEnum.OFF.value, choices=[(candle.name, candle.value) for candle in CandleEnum])
    candle_sell = models.CharField(max_length=50, choices=[(candle.name, candle.value) for candle in CandleEnum])
    candle_sell_second = models.CharField(max_length=50, default=CandleEnum.OFF.value, choices=[(candle.name, candle.value) for candle in CandleEnum])
    class Meta:
        db_table = table.CANDLE
