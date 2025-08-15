from rest_framework import serializers

from .models import Trading


class TradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trading
        fields = '__all__'
