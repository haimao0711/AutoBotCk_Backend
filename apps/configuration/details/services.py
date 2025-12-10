from common.errors.messages import ErrorMessages
from common.errors.types import ErrorType
from common.success.types import SuccessType

from collections import defaultdict
from operator import itemgetter

from apps.configuration.candle.services import CandleService
from apps.authencation.user.models import User
from ..type.enums import ConfigurationTypeEnum
from .template.services import ConfigurationTemplateServices
from ..type.services import ConfigurationTypeServices
from ..type.serializers import ConfigurationTypeSerializer
from .models import Configuration
from .serializers import ConfigurationSerializers


class ConfigurationServices:
    @staticmethod
    def is_exist_configuration(user, stock_id):
        trading = ConfigurationTypeServices.get_trading()
        try:
            _ = Configuration.objects.get(
                user=user, config_type=trading.id, stock=stock_id)
            return True
        except Configuration.DoesNotExist:
            return False

    @staticmethod
    def get_trading_configuration(user, stock_id):
        trading = ConfigurationTypeServices.get_trading()
        try:
            config_trading = Configuration.objects.get(
                user=user, config_type=trading.id, stock=stock_id)
            return config_trading
        except Configuration.DoesNotExist:
            return None

    @staticmethod
    def get_following_configuration(user, stock_id):
        following = ConfigurationTypeServices.get_following()
        try:
            config_following = Configuration.objects.get(
                user=user, config_type=following.id, stock=stock_id)
            return config_following
        except Configuration.DoesNotExist:
            return None

    @staticmethod
    def get_overview_configuration(user, stock_id, account_id):
        overview = ConfigurationTypeServices.get_overview()
        try:
            config_overview = Configuration.objects.get(
                user=user, config_type=overview.id, stock=stock_id, account=account_id)
            return config_overview
        except Configuration.DoesNotExist:
            return None

    @staticmethod
    def get_details_configutation_by_config_type(user, config_type, stock):
        try:
            config = Configuration.objects.get(
                user=user, config_type=config_type, stock_id=stock)
            return True, config
        except Configuration.DoesNotExist as error:
            return False, {}

    @staticmethod
    def get_config_type_configuration(user, config_type, stock_id):
        if ConfigurationTemplateServices.check_template_is_exist(user=user) == False:
            return {}
        if config_type == ConfigurationTypeEnum.TRADING.value:
            data = ConfigurationServices.get_trading_configuration(
                user=user, stock_id=stock_id)
            if not data:
                return {}
            return_data = ConfigurationServices.convert_data_template(
                template_data=data.__dict__)
            chart_second = None
            chart_sell = None
            chart_sell_second = None
            if data.candle_sell and data.candle_sell.candle_sell:
                chart_sell = data.candle_sell.candle_sell
            elif data.candle and data.candle.candle:
                chart_sell = data.candle.candle
            if data.candle_second and data.candle_second.candle_second:
                chart_second = data.candle_second.candle_second
            elif data.candle and data.candle.candle:
                chart_second = data.candle.candle
            if data.candle_sell_second and data.candle_sell_second.candle_sell_second:
                chart_sell_second = data.candle_sell_second.candle_sell_second
            elif data.candle and data.candle.candle:
                chart_sell_second = data.candle.candle
            return_data['chart'] = data.candle.candle
            return_data['chart_second'] = chart_second
            return_data['chart_sell'] = chart_sell
            return_data['chart_sell_second'] = chart_sell_second
            return_data['chart_type'] = data.config_type.configuration_type
            return_data['is_use_chart_second'] = data.is_use_candle_second
            return_data['stock_id'] = data.stock.id
            return_data['stock_name'] = data.stock.name
            return return_data
        elif config_type == ConfigurationTypeEnum.FOLLOWING.value:
            data = ConfigurationServices.get_following_configuration(
                user=user, stock_id=stock_id)
            
            if not data:
                return {}
            
            return_data = ConfigurationServices.convert_data_template(
                template_data=data.__dict__)
            chart_second = None
            chart_sell = None
            chart_sell_second = None

            if data.candle_sell and data.candle_sell.candle_sell:
                chart_sell = data.candle_sell.candle_sell
            elif data.candle and data.candle.candle:
                chart_sell = data.candle.candle
            if data.candle_second and data.candle_second.candle_second:
                chart_second = data.candle_second.candle_second
            elif data.candle and data.candle.candle:
                chart_second = data.candle.candle
            if data.candle_sell_second and data.candle_sell_second.candle_sell_second:
                chart_sell_second = data.candle_sell_second.candle_sell_second
            elif data.candle and data.candle.candle:
                chart_sell_second = data.candle.candle
            return_data['chart'] = data.candle.candle
            return_data['chart_second'] = chart_second
            return_data['chart_sell'] = chart_sell
            return_data['chart_sell_second'] = chart_sell_second
            return_data['chart_type'] = data.config_type.configuration_type
            return_data['is_use_chart_second'] = data.is_use_candle_second
            return_data['stock_id'] = data.stock.id
            return_data['stock_name'] = data.stock.name
            return return_data
        else:
            return {}

    @staticmethod
    def update_config_type_configuration(user, update_data):
        print('đã chạy hàm update_config_type_configuration')
        vnindex_config = update_data.get('vnindex_config')
        stock_config = update_data.get('stock_config')
        template, check, config_template = None, True, None
        stock_id = update_data.get('stock_id')
        config_type = update_data.get('chart_type')
        candle_type = update_data.get('chart')
        candle_sell_type = update_data.get('chart_sell')
        # print('check update_data: ', update_data)
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        elif config_type == ConfigurationTypeEnum.FOLLOWING.value:
            template = ConfigurationTypeServices.get_following()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check:
            return ErrorType.UPDATE_FAILED, {}

        candle = CandleService.get_candle(candle_type=candle_type)
        candle_sell = CandleService.get_candle_sell(candle_sell_type=candle_sell_type)
        # init update data
        update_config_type_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': stock_id,
            'candle': candle.id,
            'candle_sell': candle_sell.id,
            'account': None,
        }
        # print('check update_config_type_data: ', update_config_type_data)
        # handle input case
        if 'is_buy' in update_data and config_template.is_buy != update_data['is_buy']:
            update_config_type_data['is_buy'] = update_data['is_buy']

        if 'is_sell' in update_data and config_template.is_sell != update_data['is_sell']:
            update_config_type_data['is_sell'] = update_data['is_sell']

        if 'is_use_vnindex_config' in update_data and config_template.is_use_vnindex_config != update_data['is_use_vnindex_config']:
            update_config_type_data['is_use_vnindex_config'] = update_data['is_use_vnindex_config']

        if 'is_use_stock_config' in update_data and config_template.is_use_stock_config != update_data['is_use_stock_config']:
            update_config_type_data['is_use_stock_config'] = update_data['is_use_stock_config']

        for key, value in vnindex_config.items():
            update_config_type_data[f"vnindex_config_{key}"] = value

        for key, value in stock_config.items():
            update_config_type_data[f"stock_config_{key}"] = value

        try:
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['stock_name'] = data.stock.name
                return_data['chart'] = candle_type
                return_data['chart_sell'] = candle_sell_type
                return_data['chart_type'] = config_type
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}

    @staticmethod
    def update_all_config_type_configuration(user, update_data):
        print('đã chạy hàm update_all_config_type_configuration')
        vnindex_config = update_data.get('vnindex_config', {})
        stock_config = update_data.get('stock_config', {})
        config_type = update_data.get('chart_type')
        candle_type = update_data.get('chart')
        candle_sell_type = update_data.get('chart_sell')
        
        # Lấy config_type template theo chart_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
        elif config_type == ConfigurationTypeEnum.FOLLOWING.value:
            template = ConfigurationTypeServices.get_following()
        else:
            return ErrorType.UPDATE_FAILED, {'error': 'Invalid chart_type'}

        # Lấy toàn bộ cấu hình user có cùng config_type
        all_configs = Configuration.objects.filter(user=user, config_type=template.id)
        if not all_configs.exists():
            return ErrorType.UPDATE_FAILED, {'error': 'No matching configurations found for user.'}

        candle = CandleService.get_candle(candle_type=candle_type)
        candle_sell = CandleService.get_candle_sell(candle_sell_type=candle_sell_type)

        result_list = []

        for config_template in all_configs:
            update_config_type_data = {
                'config_type': template.id,
                'user': user.id,
                'stock': config_template.stock.id,
                'candle': candle.id,
                'candle_sell': candle_sell.id,
                'account': None,
            }

            # Chỉ cập nhật nếu khác giá trị hiện tại
            if 'is_buy' in update_data and config_template.is_buy != update_data['is_buy']:
                update_config_type_data['is_buy'] = update_data['is_buy']

            if 'is_sell' in update_data and config_template.is_sell != update_data['is_sell']:
                update_config_type_data['is_sell'] = update_data['is_sell']

            if 'is_use_vnindex_config' in update_data and config_template.is_use_vnindex_config != update_data['is_use_vnindex_config']:
                update_config_type_data['is_use_vnindex_config'] = update_data['is_use_vnindex_config']

            if 'is_use_stock_config' in update_data and config_template.is_use_stock_config != update_data['is_use_stock_config']:
                update_config_type_data['is_use_stock_config'] = update_data['is_use_stock_config']

            for key, value in vnindex_config.items():
                update_config_type_data[f"vnindex_config_{key}"] = value

            for key, value in stock_config.items():
                update_config_type_data[f"stock_config_{key}"] = value

            try:
                template_serializer = ConfigurationSerializers(
                    config_template, data=update_config_type_data, partial=True
                )

                if template_serializer.is_valid():
                    data = template_serializer.save()
                    return_data = ConfigurationServices.convert_data_template(
                        ConfigurationSerializers(data).data
                    )
                    return_data['stock_id'] = config_template.stock.id
                    return_data['stock_name'] = data.stock.name
                    return_data['chart'] = candle_type
                    return_data['chart_sell'] = candle_sell_type
                    return_data['chart_type'] = config_type
                    result_list.append({
                        'stock_id': config_template.stock.id,
                        'status': SuccessType.UPDATED_SUCCESS,
                        'data': return_data
                    })
                else:
                    result_list.append({
                        'stock_id': config_template.stock.id,
                        'status': ErrorType.UPDATE_FAILED,
                        'data': {'errors': {'message': str(template_serializer.errors)}}
                    })
            except Exception as error:
                result_list.append({
                    'stock_id': config_template.stock.id,
                    'status': ErrorType.UPDATE_FAILED,
                    'data': {'errors': {'message': str(error)}}
                })
        return SuccessType.UPDATED_SUCCESS, result_list


    @staticmethod
    def update_use_take_profit_first_part_false(user, stock_id, use_take_profit_first_part):
        
        # Bước 1: Lấy config_type 'trading'
        config_type = ConfigurationTypeEnum.TRADING.value
        template, check, config_template = None, True, None

        # Lấy template theo config_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check or not config_template:
            return ErrorType.UPDATE_FAILED, {}

        # Bước 2: Tạo dữ liệu cập nhật chỉ cho trường stock_config_use_take_profit_first_part
        if use_take_profit_first_part:
            update_config_type_data = {
                'config_type': template.id,
                'user': user.id,
                'stock': stock_id,
                'stock_config_use_take_profit_first_part': False  # Chỉ cập nhật trường này
            }
        else:
            update_config_type_data = {
                'config_type': template.id,
                'user': user.id,
                'stock': stock_id,
                'stock_config_use_take_profit_first_part_two': False  # Chỉ cập nhật trường này
            }

        try:
            # Cập nhật qua serializer
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()

                # Chuyển đổi dữ liệu trả về nếu cần thiết
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['chart_type'] = config_type
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}

    @staticmethod
    def update_use_bolinger_to_take_profit_a_part_false(user, stock_id):
        
        # Bước 1: Lấy config_type 'trading'
        config_type = ConfigurationTypeEnum.TRADING.value
        template, check, config_template = None, True, None

        # Lấy template theo config_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check or not config_template:
            return ErrorType.UPDATE_FAILED, {}

        # Bước 2: Tạo dữ liệu cập nhật chỉ cho trường stock_config_use_bolinger_a_part_to_take_profit
        update_config_type_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': stock_id,
            'stock_config_use_bolinger_a_part_to_take_profit': False  
        }

        try:
            # Cập nhật qua serializer
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()

                # Chuyển đổi dữ liệu trả về nếu cần thiết
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['chart_type'] = config_type
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}
    @staticmethod
    def update_use_stoch_rsi_to_take_profit_false(user, stock_id):
        
        # Bước 1: Lấy config_type 'trading'
        config_type = ConfigurationTypeEnum.TRADING.value
        template, check, config_template = None, True, None

        # Lấy template theo config_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check or not config_template:
            return ErrorType.UPDATE_FAILED, {}

        # Bước 2: Tạo dữ liệu cập nhật chỉ cho trường stock_config_use_stoch_rsi_to_take_profit
        update_config_type_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': stock_id,
            'stock_config_use_stoch_rsi_to_take_profit': False  
        }
        try:
            # Cập nhật qua serializer
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['chart_type'] = config_type
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}
    
    @staticmethod
    def update_all_take_profit_flags_false(user, stock_id, use_take_profit_first_part):
        """
        Hàm kết hợp để update cùng lúc 3 flag:
        - stock_config_use_bolinger_a_part_to_take_profit = False
        - stock_config_use_stoch_rsi_to_take_profit = False
        - stock_config_use_take_profit_first_part hoặc stock_config_use_take_profit_first_part_two = False
        - stock_config_use_rsi_decrease_to_take_profit = False
        """
        # Bước 1: Lấy config_type 'trading'
        config_type = ConfigurationTypeEnum.TRADING.value
        template, check, config_template = None, True, None

        # Lấy template theo config_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check or not config_template:
            return ErrorType.UPDATE_FAILED, {}

        # Bước 2: Tạo dữ liệu cập nhật cho 4 trường cùng lúc
        update_config_type_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': stock_id,
            'stock_config_use_bolinger_a_part_to_take_profit': False,
            'stock_config_use_stoch_rsi_to_take_profit': False,
            'stock_config_use_rsi_decrease_to_take_profit': False
        }
        
        # Thêm flag tùy theo use_take_profit_first_part
        if use_take_profit_first_part:
            update_config_type_data['stock_config_use_take_profit_first_part'] = False
        else:
            update_config_type_data['stock_config_use_take_profit_first_part_two'] = False

        try:
            # Cập nhật qua serializer
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()

                # Chuyển đổi dữ liệu trả về nếu cần thiết
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['chart_type'] = config_type
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}
    
    @staticmethod
    def update_is_trading_configuration(user, stock_id, is_trading):

        # Bước 1: Lấy config_type 'trading'
        config_type = ConfigurationTypeEnum.TRADING.value
        template, check, config_template = None, True, None

        # Lấy template theo config_type
        if config_type == ConfigurationTypeEnum.TRADING.value:
            template = ConfigurationTypeServices.get_trading()
            check, config_template = ConfigurationServices.get_details_configutation_by_config_type(
                user=user, config_type=template.id, stock=stock_id)
        else:
            return ErrorType.UPDATE_FAILED, {}

        if not check or not config_template:
            return ErrorType.UPDATE_FAILED, {}

        # Bước 2: Tạo dữ liệu cập nhật chỉ cho trường is_trading
        update_config_type_data = {
            'config_type': template.id,
            'user': user.id,
            'stock': stock_id,
            'is_trading': is_trading  # Chỉ cập nhật trường này
        }

        try:
            # Cập nhật qua serializer
            template_serializer = ConfigurationSerializers(
                config_template, data=update_config_type_data, partial=True)

            if template_serializer.is_valid():
                data = template_serializer.save()

                # Chuyển đổi dữ liệu trả về nếu cần thiết
                return_data = ConfigurationServices.convert_data_template(
                    ConfigurationSerializers(data).data)
                return_data['stock_id'] = stock_id
                return_data['chart_type'] = config_type

                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                errors = template_serializer.errors
                return ErrorType.UPDATE_FAILED, {'errors': {'message': str(errors)}}
        except Exception as error:
            return ErrorType.UPDATE_FAILED, {'errors': {'message': str(error)}}

    


    @staticmethod
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

    @staticmethod
    def get_all_user_configuration(user: User):
        configurations = Configuration.objects.filter(user=user)
  
        # Initialize the result dictionary
        user_configurations = {}

        # Iterate through configurations
        for config in configurations:
            if not config.stock:
                continue
            stock_id = config.stock.name

            # Check if the stock_id is not already in the result dictionary
            if stock_id not in user_configurations:
                user_configurations[stock_id] = {
                    'stock': config.stock,
                    'trading_config': None,
                    'following_config': None,
                    'overview_config': {}
                }

            # Check config_type and assign to the appropriate key
            if config.config_type_id == 2:  # Trading
                user_configurations[stock_id]['trading_config'] = config
            elif config.config_type_id == 3:  # Following
                user_configurations[stock_id]['following_config'] = config
            elif config.config_type_id == 4:  # Overview
                # Check if the config has an account associated with it
                if config.account.name:
                    user_configurations[stock_id]['overview_config'][config.account.name] = config

        return user_configurations

    @staticmethod
    def get_and_sort_user_configuration_by_level(user: User):
        # Query all configurations for the given user
        configurations = Configuration.objects.filter(user=user)

        # Initialize dictionaries and lists
        user_configurations = {}
        overview_unsorted = []

        # Iterate through configurations
        for config in configurations:
            if not config.stock:
                continue
            stock_id = config.stock.name

            # Initialize stock configuration if not already present
            if stock_id not in user_configurations:
                user_configurations[stock_id] = {
                    'stock': config.stock,
                    'trading_config': None,
                    'following_config': None,
                    'overview_config': []
                }

            # Assign configurations based on type
            if config.config_type_id == 2:  # Trading
                user_configurations[stock_id]['trading_config'] = config
            elif config.config_type_id == 3:  # Following
                user_configurations[stock_id]['following_config'] = config
            elif config.config_type_id == 4:  # Overview
                overview_unsorted.append({
                    'stock': config.stock,
                    'overview_config': config,
                    'level': config.level
                })

        # Sort overview configurations by level
        sorted_overview = sorted(
            overview_unsorted,
            key=lambda x: x['level']
        )

        # Attach sorted overview configurations to stock configurations
        for overview in sorted_overview:
            for stock, object_config in user_configurations.items():
                stock_of_overview = overview.get('stock').symbol
                if stock_of_overview == stock:
                    overview['trading_config'] = object_config.get(
                        'trading_config')
                    overview['following_config'] = object_config.get(
                        'following_config')
                    break
                else:
                    continue

        return sorted_overview

    @staticmethod
    def get_user_configuration_by_stock_symbol(user: User, stock_symbol: str):
        # Query all configurations for the given user
        configurations = Configuration.objects.filter(user=user)

        # Khởi tạo dict để lưu theo stock
        user_configurations = {}
        overview_unsorted = []

        # Duyệt qua tất cả configurations
        for config in configurations:
            if not config.stock:
                continue
            stock_id = config.stock.symbol  # So sánh bằng symbol (mã cổ phiếu)

            if stock_id != stock_symbol:
                continue  # Bỏ qua nếu không phải mã cổ phiếu cần tìm

            # Khởi tạo config cho cổ phiếu nếu chưa có
            if stock_id not in user_configurations:
                user_configurations[stock_id] = {
                    'stock': config.stock,
                    'trading_config': None,
                    'following_config': None,
                    'overview_config': []
                }

            # Gán theo loại config
            if config.config_type_id == 2:  # Trading
                user_configurations[stock_id]['trading_config'] = config
            elif config.config_type_id == 3:  # Following
                user_configurations[stock_id]['following_config'] = config
            elif config.config_type_id == 4:  # Overview
                overview_unsorted.append({
                    'stock': config.stock,
                    'overview_config': config,
                    'level': config.level
                })

        # Nếu không có overview nào thì trả về None
        if not overview_unsorted:
            return None

        # Sắp xếp overview theo level
        sorted_overview = sorted(overview_unsorted, key=lambda x: x['level'])

        # Lấy phần tử đầu tiên (có level thấp nhất)
        overview = sorted_overview[0]
        stock_id = overview['stock'].symbol

        # Gán thêm trading và following nếu có
        if stock_id in user_configurations:
            overview['trading_config'] = user_configurations[stock_id].get('trading_config')
            overview['following_config'] = user_configurations[stock_id].get('following_config')

        return overview


    @staticmethod
    def update_volume_to_buy(user_id: int, stock_id: int, account_id: int, value: float, type: str):
        if type not in ['increase', 'decrease']:
            return

        config = ConfigurationServices.get_overview_configuration(
            user_id, stock_id, account_id)

        if config is None:
            return
        if type == 'increase':
            config.volume_to_buy += value
        if type == 'decrease':
            config.volume_to_buy -= value
        config.save()
