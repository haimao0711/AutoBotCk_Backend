from common.errors.messages import ErrorMessages

from .models import ConfigurationType
from .enums import ConfigurationTypeEnum

class ConfigurationTypeServices:
    def check_configuration_type_exist(type):
        try:
            _ = ConfigurationType.objects.get(configuration_type=type)
            return True
        except (ConfigurationType.DoesNotExist):
            return False
    
    def is_template_configuration(type):
        if type == ConfigurationTypeEnum.TEMPLATE.value:
            return True
        return False
    
    def is_following_configuration(type):
        if type == ConfigurationTypeEnum.FOLLOWING.value:
            return True
        return False
    
    def is_trading_configuration(type):
        if type == ConfigurationTypeEnum.TRADING.value:
            return True
        return False
    
    def is_overview_configuration(type):
        if type == ConfigurationTypeEnum.OVERVIEW.value:
            return True
        return False
    
    def get_template():
        template = ConfigurationTypeEnum.TEMPLATE.value
        return ConfigurationType.objects.get(configuration_type=template)
    
    def get_trading():
        trading = ConfigurationTypeEnum.TRADING.value
        return ConfigurationType.objects.get(configuration_type=trading)
    
    def get_following():
        following = ConfigurationTypeEnum.FOLLOWING.value
        return ConfigurationType.objects.get(configuration_type=following)
    
    def get_overview():
        overview = ConfigurationTypeEnum.OVERVIEW.value
        return ConfigurationType.objects.get(configuration_type=overview)
    def get_overview_user(user):
        overview = ConfigurationTypeEnum.OVERVIEW.value
        instance = ConfigurationType.objects.filter(user=user, configuration_type=overview).first()
        if not instance:
            raise ValueError("No overview configuration found for this user")
        return instance

