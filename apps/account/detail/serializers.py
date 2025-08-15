from rest_framework import serializers

from .models import Account, SubAccount


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class SubAccountSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(
        source='account_type.name', read_only=True)

    class Meta:
        model = SubAccount
        fields = ['id', 'main_account', 'account_type',
                  'account_type_name', 'name', 'amount', 'balance', 'valid']
