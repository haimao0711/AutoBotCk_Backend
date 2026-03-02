from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import Configuration

class ConfigurationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        update_fields = set()
        
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                update_fields.add(attr)

        if update_fields:
            instance.save(update_fields=list(update_fields))
        else:
            instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

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

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        update_fields = set()
        
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                update_fields.add(attr)

        if update_fields:
            instance.save(update_fields=list(update_fields))
        else:
            instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance