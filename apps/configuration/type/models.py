from django.db import models

from .enums import ConfigurationTypeEnum

import common.table_names as table

class ConfigurationType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    configuration_type = models.CharField(
        max_length=50,
        choices=[(configuration.name, configuration.value) for configuration in ConfigurationTypeEnum])
    
    class Meta:
        db_table = table.CONFIGURATION_TYPE
