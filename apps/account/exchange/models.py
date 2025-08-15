from django.db import models

from .enums import ExchangeTypeEnum

import common.table_names as table

class Exchange(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    exchange_type = models.CharField(max_length=50, choices=[(exchange.name, exchange.value) for exchange in ExchangeTypeEnum])
    website = models.CharField(max_length=50)
    
    class Meta:
        db_table = table.EXCHANGE
