from django.db import models
from django.core.validators import MinValueValidator

from apps.authencation.user.models import User
from apps.stock.models import Stock
from apps.account.detail.models import Account

from common.validation_data import signal_type_validator
import common.table_names as table

class TransactionLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    signal_type = models.CharField(
        max_length=100, validators=[signal_type_validator])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume_set = models.FloatField(
        default=0, validators=([MinValueValidator(0)]))
    volume_match = models.FloatField(
        default=0, validators=([MinValueValidator(0)]))
    created_at = models.DateTimeField()

    class Meta:
        db_table = table.TRANSACTION_LOG
