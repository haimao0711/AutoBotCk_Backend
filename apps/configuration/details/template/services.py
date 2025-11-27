from common.errors.messages import ErrorMessages
from common.success.types import SuccessType
from common.errors.types import ErrorType

from ..serializers import ConfigurationSerializers
from ...type.services import ConfigurationTypeServices
from ...models import Configuration
from ...candle.enums import CandleEnum
from ...type.enums import ConfigurationTypeEnum


class ConfigurationTemplateServices:

    @staticmethod
    def get_base_configuration_template(user):
        template = ConfigurationTypeServices.get_template()
        try:
            config_template = Configuration.objects.get(
                user=user, config_type=template.id, stock=None)
            return ConfigurationSerializers(config_template).data
        except Configuration.DoesNotExist:
            return {}

    def get_configuration_template(user):
        template = ConfigurationTypeServices.get_template()

        try:
            config_template = Configuration.objects.get(user=user, config_type=template.id, stock=None)
        except Configuration.DoesNotExist:
            # try:
            #     # Nếu không tìm thấy, lấy template của user_id = 3
            #     base_template = Configuration.objects.get(user_id=3, config_type=template.id, stock=None)
            #     # Tạo một bản sao mới cho user hiện tại
            #     config_template = Configuration.objects.create(
            #         user=user,
            #         config_type=template.id,
            #         config_data=base_template.config_data  # Giữ nguyên dữ liệu của user_id=3
            #     )
            # except Configuration.DoesNotExist:
                return {}

        return ConfigurationTemplateServices.convert_data_template(ConfigurationSerializers(config_template).data)


    @staticmethod
    def create_a_new_configuration_template(user, template_data):
        base_config = template_data.get('config', {})
        vnindex_config = template_data.get('vnindex_config', {})
        stock_config = template_data.get('stock_config', {})
        template = ConfigurationTypeServices.get_template()

        init_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': None,
            'candle': None,
            'account': None
        }

        for key, value in base_config.items():
            init_data[key] = value

        for key, value in vnindex_config.items():
            init_data[f"vnindex_config_{key}"] = value

        for key, value in stock_config.items():
            init_data[f"stock_config_{key}"] = value

        try:
            template_serializers = ConfigurationSerializers(data=init_data)
            if template_serializers.is_valid():
                config_template = template_serializers.save()
                data = ConfigurationTemplateServices.convert_data_template(
                    ConfigurationSerializers(config_template).data)
                return SuccessType.CREATE_SUCCESS, data
            else:
                errors = template_serializers.errors
                return ErrorType.CREATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.CREATE_FAILED, {'errors': {'message': str(error)}}

    def create_configuration_template(user, template_data):
        if ConfigurationTemplateServices.check_template_is_exist(user):
            return SuccessType.CREATE_SUCCESS, ConfigurationTemplateServices.get_configuration_template(user)
        return ConfigurationTemplateServices.create_a_new_configuration_template(user, template_data)

    def update_a_exist_configuration_template(user, template_data_update):
        vnindex_config = template_data_update.get('vnindex_config')
        stock_config = template_data_update.get('stock_config')
        template = ConfigurationTypeServices.get_template()

        config_template = Configuration.objects.get(
            user=user, config_type=template.id, stock=None)

        # init update data

        update_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': None,
            'candle': None,
            'account': None,
        }

        # handle input case

        if 'is_buy' in template_data_update and config_template.is_buy != template_data_update['is_buy']:
            update_data['is_buy'] = template_data_update['is_buy']

        if 'is_sell' in template_data_update and config_template.is_sell != template_data_update['is_sell']:
            update_data['is_sell'] = template_data_update['is_sell']

        if 'is_use_vnindex_config' in template_data_update and config_template.is_use_vnindex_config != template_data_update['is_use_vnindex_config']:
            update_data['is_use_vnindex_config'] = template_data_update['is_use_vnindex_config']

        if 'is_use_stock_config' in template_data_update and config_template.is_use_stock_config != template_data_update['is_use_stock_config']:
            update_data['is_use_stock_config'] = template_data_update['is_use_stock_config']

        for key, value in vnindex_config.items():
            update_data[f"vnindex_config_{key}"] = value

        for key, value in stock_config.items():
            update_data[f"stock_config_{key}"] = value

        try:
            template_serializer = ConfigurationSerializers(
                config_template, data=update_data, partial=True)

            if template_serializer.is_valid():
                template_serializer.save()
                data = ConfigurationTemplateServices.convert_data_template(
                    ConfigurationSerializers(config_template).data)
                return SuccessType.UPDATED_SUCCESS, data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}

    def update_configuration_template(user, template_data_update):
        print('đã vào hàm update_configuration_template ')
        if ConfigurationTemplateServices.check_template_is_exist(user):
            print('đã thỏa mãn check_template_is_exist ')
            return ConfigurationTemplateServices.update_a_exist_configuration_template(user, template_data_update)
        else: 
            print('chưa thỏa mãn check_template_is_exist ')
            ConfigurationTemplateServices.create_configuration_template(user, template_data_update)
            return ConfigurationTemplateServices.update_a_exist_configuration_template(user, template_data_update)
        return ErrorType.UPDATE_FAILED, {}

    def check_template_is_exist(user):
        template = ConfigurationTypeServices.get_template()

        try:
            _ = Configuration.objects.get(user=user, config_type=template.id, stock=None)
            return True
        except Configuration.DoesNotExist:
            return False

    def convert_data_template(template_data):
        vnindex_config = {}
        stock_config = {}

        for key, value in template_data.items():
            if key.startswith('vnindex_config'):
                new_key = key[len('vnindex_config_'):]
                vnindex_config[new_key] = value
            elif key.startswith('stock_config'):
                new_key = key[len('stock_config_'):]
                stock_config[new_key] = value

        return {
            'id': template_data.get('id'),
            'is_buy': template_data.get('is_buy'),
            'is_sell': template_data.get('is_sell'),
            'is_use_stock_config': template_data.get('is_use_stock_config'),
            'is_use_vnindex_config': template_data.get('is_use_vnindex_config'),
            'vnindex_config': vnindex_config,
            'stock_config': stock_config,
            'level': template_data.get('level')
        }
