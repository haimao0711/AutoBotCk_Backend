from rest_framework import serializers

from .models import Candle

class CandleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = '__all__'
