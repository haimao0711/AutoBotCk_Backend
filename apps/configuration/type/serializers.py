from rest_framework import serializers

from .models import ConfigurationType

class ConfigurationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationType
        fields = '__all__'
