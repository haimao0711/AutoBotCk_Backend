from django.db import models
from apps.account.detail.models import Account

import common.table_names as table


class AccountTradingLimits(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True)
    limit = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Limit of {self.account}: {self.limit}'

    class Meta:
        db_table = table.LIMITS_TRADING
