from rest_framework import serializers
from .models import AccountTradingLimits


class AccountTradingLimitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTradingLimits
        fields = "__all__"
