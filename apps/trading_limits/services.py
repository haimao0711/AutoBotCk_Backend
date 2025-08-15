from django.db import IntegrityError
from .models import AccountTradingLimits
from django.contrib import messages


class AccountTradingLimitsServices:

    @staticmethod
    def get_trading_limits_account(account_id: int):
        try:
            account = AccountTradingLimits.objects.get(account=account_id)
            return account
        except Exception as error:
            return None

    @staticmethod
    def create_limits_base_account(account_id: int, limits: int):
        if limits < 0:
            messages.error("Limits must be a non-negative integer.")
            return

        try:
            existing_limit = AccountTradingLimits.objects.filter(
                account_id=account_id).first()
            if existing_limit:
                existing_limit.limit = limits
                existing_limit.save()
            else:
                AccountTradingLimits.objects.create(
                    account_id=account_id, limit=limits)
        except IntegrityError:
            messages.error("Database error occurred while creating limits.")

    @staticmethod
    def update_limits_base_account(account_id: int, limits: int):
        if limits < 0:
            messages.error("Limits must be a non-negative integer.")
            return

        try:
            trading_limit = AccountTradingLimits.objects.filter(
                account_id=account_id).first()
            if trading_limit:
                trading_limit.limit = limits
                trading_limit.save()
            else:
                messages.error(
                    "Trading limits record does not exist for the given account.")
        except IntegrityError:
            messages.error("Database error occurred while updating limits.")
