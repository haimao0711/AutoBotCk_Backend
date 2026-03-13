from django.db import models
from django.core.validators import MinValueValidator

from ..exchange.models import Exchange

import common.table_names as table

from .enums import AccountStatusEnum, AccountLoginStatusEnum


class Account(models.Model):

    # Init fileds
    name = models.CharField(max_length=100)
    account_num = models.CharField(max_length=10, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, default='')
    is_need_otp = models.BooleanField(default=False)
    exchange = models.ForeignKey(
        Exchange, on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.CharField(max_length=100, default='Khách hàng')
    # Generates fields
    vps_cookie = models.CharField(null=True)
    vps_request_verify_token = models.CharField(null=True)
    vps_hash_password = models.CharField(null=True)
    vps_session_id = models.CharField(null=True)
    vps_channel = models.CharField(null=True, default='I')

    # status of login fields
    status_choices = [(status.name, status.value)
                      for status in AccountStatusEnum]
    login_status_choices = [(status.name, status.value)
                            for status in AccountLoginStatusEnum]
    status = models.CharField(
        max_length=100, choices=status_choices, default=AccountStatusEnum.Active.value)
    login_status = models.CharField(
        max_length=100, choices=login_status_choices, default=AccountLoginStatusEnum.LoginFailed.value)
    is_block_buy = models.BooleanField(default=False)
    is_block_sell = models.BooleanField(default=False)
    limit_number_stocks = models.IntegerField(default=10)
    limit_total_market_value = models.IntegerField(default=500000000)
    def __str__(self):
        return f"Account:\nName: {self.name}\nAlias name: {self.alias}\nStatus: {self.status}\nLogin_status: {self.login_status}"

    class Meta:
        db_table = table.ACCOUNT


class AccountType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = table.ACCOUNT_TYPE


class SubAccount(models.Model):

    main_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    amount = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_balance = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    valid = models.BooleanField(default=False)

    def _str__(self):
        return f'{self.name}-{self.account_type.name}: {self.valid}'

    class Meta:
        db_table = table.SUBACCOUNT
