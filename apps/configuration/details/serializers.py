from rest_framework import serializers

from .models import Configuration

class ConfigurationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

class TradeHandleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = [
            'is_update_volume_buy', 'is_use_price_to_buy', 'is_block_buy', 'is_block_sell',
            'is_use_stoploss', 'is_use_takeprofit', 'price_to_buy_now', 'is_buy_hand', 
            'is_sell_hand','volume_to_buy', 'margin_percentage', 'level'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}

    def validate(self, data):
        if not any(field in data for field in self.fields):
            raise serializers.ValidationError("Phải có ít nhất một trường được truyền vào.")
        return data