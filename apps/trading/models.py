import apps.trading.service
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.configuration.details.models import Configuration
from apps.stock.models import Stock
from apps.trading.enum.enums import StatusPidEnum

import common.table_names as table


class Trading(models.Model):

    _STATUS_CHOICES = [
        ('waiting_to_buy', 'Waiting to Buy'),
        ('ready_to_buy', 'Ready to Buy'),
        ('buying_processing', 'Buying Processing'),
        ('waiting_to_sell', 'Waiting to Sell'),
        ('ready_to_sell', 'Ready to Sell'),
        ('selling_processing', 'Selling Processing'),
        ('completed', 'Completed')
    ]

    base_configuration = models.OneToOneField(
        Configuration, on_delete=models.CASCADE, related_name='base_configuration')
    status_pid = models.CharField(max_length=50, choices=[(
        status.name, status.value) for status in StatusPidEnum])
    max_volume_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    volume_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    volume_sell = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    aver_price_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    profit = models.FloatField(default=0, validators=[MinValueValidator(0)])

    trading_status = models.CharField(
        max_length=20, choices=_STATUS_CHOICES, default='ready_to_buy')
    last_status_change = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = table.TRADING
