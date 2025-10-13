from django.db import transaction

from common.errors.messages import ErrorMessages
from common.success.types import SuccessType
from common.errors.types import ErrorType
from common.calculator import calculate_profit, calculate_stoploss

from apps.stock.services import StockService, DownloadService
from apps.stock.models import StockM1, StockD1
from apps.configuration.candle.enums import CandleEnum
from apps.stock.enums import DownloadStatusEnum

from apps.account.detail.services import AccountService
from apps.configuration.details.serializers import ConfigurationSerializers, TradeHandleSerializers
from apps.configuration.candle.services import CandleService
from apps.account.user_account.services import UserAccountService
from apps.configuration.details.services import ConfigurationServices
from apps.trading.services import TradingService
from apps.trading.enum.enums import StatusPidEnum
from apps.trading.serializers import TradingSerializer
# from apps.balance.models import SubAccountBalance
# from apps.balance.serializers import SubAccountBalanceSerializer
# from apps.balance.services import BalanceService
from ..template.services import ConfigurationTemplateServices
from ...details.models import Configuration
from ...type.services import ConfigurationTypeServices
from concurrent.futures import ThreadPoolExecutor
from apps.authencation.user.models import User
from apps.account.detail.models import Account
from common.api.smartone.api import  get_stock_balance
from apps.stockSocket.services.cache_service import get_price
from apps import api
import json

class ConfigurationOverviewServices:
  
    def get_detail_stock_configuration(user, stock_id):
        overview = ConfigurationTypeServices.get_overview()

        try:
            configurations = Configuration.objects.get(
                user=user, config_type=overview.id, stock_id=stock_id)
            return ConfigurationSerializers(configurations).data

        except Configuration.DoesNotExist:
            return {}
    def get_detail_stock_configurations(user):
        # print('Bat dau hàm get_detail_stock_configurations')
        overview = ConfigurationTypeServices.get_overview()
        try:
            configurations = Configuration.objects.filter(
                user=user, config_type=overview.id
            ).select_related( 'stock', 'config_type' )
            configurations_following = Configuration.objects.filter(
                user=user, config_type=following.id
            ).select_related( 'stock', 'following' )
            configurations_trading = Configuration.objects.filter(
                user=user, config_type=trading.id
            ).select_related( 'stock', 'trading' )
            stock_ids = [config.stock.id for config in configurations]
            # Lấy dữ liệu hàng loạt
            query_data_m1_all = StockService.get_last_stock_chart_items_by_time_bulk(
                StockModel=StockM1, stock_ids=stock_ids
            )
            query_data_m1_map = {item['id']: item for item in query_data_m1_all}
            config_following_map = {item['id']: item for item in configurations_following}
            config_trading_map = {item['id']: item for item in configurations_trading}
            # Chuẩn bị stock_data
            stock_data = {}
            for config in configurations:
                stock_id = config.stock.id
                # # Thêm phản hồi chart
                # data_following = ConfigurationServices.get_config_type_configuration(user=user, config_type='following', stock_id=stock_id)   
                # data_trading = ConfigurationServices.get_config_type_configuration(user=user, config_type='trading', stock_id=stock_id) 
                # following_chart_buy = data_following['chart']
                # following_chart_sell = data_following['chart_sell']
                # trading_chart_buy = data_trading['chart']
                # trading_chart_sell = data_trading['chart_sell']
                # # Xong thêm phản hồi chart
                stock_name = config.stock.name
                query_data_m1 = query_data_m1_map.get(stock_id)
                #Thêm phản hồi chart
                data_following = config_following_map.get(stock_id)
                data_trading = config_trading_map.get(stock_id)
                following_chart_buy = data_following['chart']
                following_chart_sell = data_following['chart_sell']
                trading_chart_buy = data_trading['chart']
                trading_chart_sell = data_trading['chart_sell']
                # Xong thêm phản hồi chart
                low_price = query_data_m1['low'] if query_data_m1 else 0
                high_price = query_data_m1['high'] if query_data_m1 else 0
                # current_price = get_price(stock_name)
                average_price = (float(low_price) + float(high_price)) / 2
                current_price = query_data_m1['close'] if query_data_m1 else 0

                stock_data[stock_name] = {
                    'id': stock_id,
                    'name': stock_name,
                    'low': low_price,
                    'high': high_price,
                    'close': current_price,
                    'average_price': average_price,
                    'following_chart_buy': following_chart_buy,
                    'following_chart_sell' : following_chart_sell,
                    'trading_chart_buy' : trading_chart_buy,
                    'trading_chart_sell' : trading_chart_sell,
                }
            vps_account = AccountService.get_account_by_user(user)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            request_url = api.TRADING_URL
            data_res = get_stock_balance( account_name, account_num, request_url, session_id, '')
            stock_balance_text = data_res.text
            stock_balance_object = json.loads(stock_balance_text)
            data_balance = stock_balance_object['data']
            stock_balance_data = [item for item in data_balance ]
            # Xử lý đồng thời với ThreadPoolExecutor
            def process_configuration(configuration):
                stock_name = configuration.stock.name
                current_price = stock_data[stock_name]['close']
                following_chart_buy = stock_data[stock_name]['following_chart_buy']
                following_chart_sell = stock_data[stock_name]['following_chart_sell']
                trading_chart_buy = stock_data[stock_name]['trading_chart_buy']
                trading_chart_sell = stock_data[stock_name]['trading_chart_sell']
                # trading_data = trading_data_map.get(configuration.id, {})
                balance_by_stock = next((stock for stock in stock_balance_data if stock.get('symbol') == stock_name), None)
                return {
                    'account_vps': account_name,
                    'account_vps_num': account_num,
                    'id': configuration.id,
                    'is_block_buy': configuration.is_block_buy,
                    'is_block_sell': configuration.is_block_sell,
                    'is_buy_hand': configuration.is_buy_hand,
                    'is_sell_hand': configuration.is_sell_hand,
                    'is_use_price_to_buy': configuration.is_use_price_to_buy,
                    'price_to_buy_now': configuration.price_to_buy_now,
                    'is_use_stoploss': configuration.is_use_stoploss,
                    'is_use_takeprofit': configuration.is_use_takeprofit,
                    'is_update_volume_buy': configuration.is_update_volume_buy,
                    'volume_to_buy': configuration.volume_to_buy,
                    'stock_id': configuration.stock.id,
                    'stock_name': configuration.stock.name,
                    'current_price': current_price,
                    'status_pid': 'FOLLOWING',
                    'volume_buy': balance_by_stock.get('actual_vol') if balance_by_stock else 0,
                    'volume_trade': balance_by_stock.get('avaiable_vol') if balance_by_stock else 0,
                    'aver_price_buy': balance_by_stock.get('avg_price') if balance_by_stock else 0,
                    'current_profit': balance_by_stock.get('gain_loss_per') if balance_by_stock else 0,
                    "chart_type": configuration.config_type.name,
                    "level": configuration.level,
                    'following_chart_buy': following_chart_buy,
                    'following_chart_sell' : following_chart_sell,
                    'trading_chart_buy' : trading_chart_buy,
                    'trading_chart_sell' : trading_chart_sell,
                }

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_configuration, config) for config in configurations]
                data = [future.result() for future in futures]
            # sorted_data = sorted(data, key=lambda x: int(x["volume_buy"]), reverse=True)
            # print('Kết thúc hàm get_detail_stock_configurations')
            return data

        except Exception as error:
            print('error', str(error))
            return []

    def create_a_new_overview_configuration(user, init_overview_data):
        stock = StockService.get_stock_by_id(stock_id=init_overview_data.get('stock_id'))
        print('check stock is create: ', stock)
        following = ConfigurationTypeServices.get_following()
        trading = ConfigurationTypeServices.get_trading()
        
        following_candle = CandleService.get_candle(
            candle_type=init_overview_data.get('chart_following'))
        trading_candle = CandleService.get_candle(
            candle_type=init_overview_data.get('chart_trading'))
        
        template_data = ConfigurationTemplateServices.get_base_configuration_template(user=user)
        template_data['user'] = user.id
        template_data['stock'] = stock.id
        
        following_data = template_data.copy()
        following_data['config_type'] = following.id
        following_data['candle'] = following_candle.id
        
        trading_data = template_data.copy()
        trading_data['config_type'] = trading.id
        trading_data['candle'] = trading_candle.id
        
        return_data = []
        
        # Kiểm tra xem cấu hình đã tồn tại chưa
        if ConfigurationOverviewServices.check_is_overview_exist(user=user, stock_id=stock.id):
            overview_configuration = ConfigurationOverviewServices.get_detail_stock_configuration(user=user, stock_id=stock.id)
            return_data.append(overview_configuration)
        else:
            with transaction.atomic():
                init_data = {
                    'user': user.id,
                    'stock': stock.id,
                    'config_type': ConfigurationTypeServices.get_overview().id,
                    'is_use_price_to_buy': False,
                    'price_to_buy_now': 0.0,
                    'is_use_stoploss': False,
                    'percent_to_stoploss': 0.0,
                    'is_use_takeprofit': False,
                    'percent_to_takeprofit': 0.0,
                    'is_update_volume_buy': False,
                    'volume_to_buy': 0.0
                }
                
                overview_serializer = ConfigurationSerializers(data=init_data)
                if overview_serializer.is_valid():
                    overview = overview_serializer.save()
                else:
                    raise ValueError(str(overview_serializer.errors))
                
                StockService.download_imported_new_data_to_database_chart(stock_ids=[stock.id])
                
                # Tạo cấu hình following và trading nếu chưa tồn tại
                if not ConfigurationServices.is_exist_configuration(user=user, stock_id=stock.id):
                    following_serializer = ConfigurationSerializers(data=following_data)
                    if following_serializer.is_valid():
                        following_serializer.save()
                    else:
                        raise ValueError(str(following_serializer.errors))
                    
                    trading_serializer = ConfigurationSerializers(data=trading_data)
                    if trading_serializer.is_valid():
                        trading_serializer.save()
                    else:
                        raise ValueError(str(trading_serializer.errors))
                    
                return_data.append(init_data)
        
        return SuccessType.CREATE_SUCCESS, return_data


    def create_overview_configuration(user, init_overview_data):
        print('đã vào hàm create_overview_configuration ')
        if ConfigurationTemplateServices.check_template_is_exist(user=user):
            print('đã vào if ConfigurationTemplateServices.check_template_is_exist ')
            return ConfigurationOverviewServices.create_a_new_overview_configuration(user, init_overview_data)
        return ErrorType.CREATE_FAILED, {}

    def update_a_overview_configuration(user, update_overview_data):

        # if UserAccountService.check_account_belong_user(user=user, account=account.main_account.id) == False:
        #     return ErrorType.UPDATE_FAILED, {}
        allow_fields = ['is_update_volume_buy', 'is_use_price_to_buy', 'is_block_buy', 'is_block_sell', 'is_buy_hand', 'is_sell_hand',
                        'is_use_stoploss', 'is_use_takeprofit', 'price_to_buy_now', 'volume_to_buy', 'margin_percentage', 'level']
        update_data = {
            field: value
            for field in allow_fields
            if (value := update_overview_data.get(field)) is not None
        }

        overview_configuration = ConfigurationOverviewServices.get_overview_exist(
            user=user, stock_id=update_overview_data.get('stock_id'))


        try:
            overview_serializer = TradeHandleSerializers(
                overview_configuration, data=update_data, partial=True)
            if overview_serializer.is_valid():
                updated_instance = overview_serializer.save()
                return_data = {field: getattr(
                    updated_instance, field) for field in allow_fields}
                return_data['user'] = user.id
                return_data['stock_id'] = update_overview_data.get('stock_id')
                # return_data['account'] = update_overview_data.get(
                #     'account_id')
                return SuccessType.UPDATED_SUCCESS, return_data
            else:
                print("Serializer errors:", overview_serializer.errors)
                return ErrorType.UPDATE_FAILED, {
                    'message': str(overview_serializer.errors)
                }
        except Exception as errors:
            return ErrorType.UPDATE_FAILED, {
                'message': str(errors)
            }

    def update_overview_configuration(user, update_overview_data):
        if ConfigurationTemplateServices.check_template_is_exist(user=user):
            return ConfigurationOverviewServices.update_a_overview_configuration(user, update_overview_data)
        return ErrorType.UPDATE_FAILED, {
            'message': 'this case'
        }

    def update_block_trade_overview(user, type_block, is_block_buy, is_block_sell):
        overview_type = ConfigurationTypeServices.get_overview()

        # Lọc danh sách các bản ghi cần cập nhật
        overviews = Configuration.objects.filter(user=user, config_type=overview_type.id)

        if overviews.exists():
            # Cập nhật toàn bộ các bản ghi
            if type_block == 'B':
                overviews.update(is_block_buy=is_block_buy)
            elif type_block == 'S':
                overviews.update(is_block_sell=is_block_sell)
            return overviews  # Trả về danh sách các bản ghi đã được cập nhật

        return {}  # Không có bản ghi nào để cập nhật
    def restart_request_trade_overview(user):
        # Trả lại trạng thái ban đầu của mua bán tay và is_trading của cấu hình
        overview_type = ConfigurationTypeServices.get_overview()
        trading_type = ConfigurationTypeServices.get_trading()
        # Lọc danh sách các bản ghi cần cập nhật
        overviews = Configuration.objects.filter(user=user, config_type=overview_type.id)
        tradings = Configuration.objects.filter(user=user, config_type=trading_type.id)
        if overviews.exists():
            overviews.update(is_buy_hand=False, is_sell_hand=False)
        if tradings.exists():
            tradings.update(is_trading=False)
        return {}  # Không có bản ghi nào để cập nhật
    
    def restart_is_trading_configutation(user):
        trading_type = ConfigurationTypeServices.get_trading()

        # Lọc danh sách các bản ghi cần cập nhật
        tradings = Configuration.objects.filter(user=user, config_type=trading_type.id)

        if tradings.exists():
            tradings.update(is_trading=False)

        return {}  # Không có bản ghi nào để cập nhật

    def count_overview_configurations(user):
        overview = ConfigurationTypeServices.get_overview()

        try:
            configurations = Configuration.objects.filter(
                user=user, config_type=overview.id)
            return len(configurations)
        except Exception:
            return 0

    def count_overview_configuration(user, stock_id):
        overview = ConfigurationTypeServices.get_overview()

        try:
            configurations = Configuration.objects.filter(
                user=user, config_type=overview.id, stock=stock_id)
            return len(configurations)
        except Exception:
            return 0

    def delete_overview_configuration(user, delete_overview_data):
        stock_id = delete_overview_data.get('stock_id')

        num_of_overview = ConfigurationOverviewServices.count_overview_configuration(
            user=user, stock_id=stock_id
        )
        overview_configuration = ConfigurationOverviewServices.get_overview_exist(
            user=user, stock_id=stock_id
        )

        if num_of_overview == 0:
            return SuccessType.DELETE_SUCCESS, {}

        elif num_of_overview == 1:
            with transaction.atomic():
                trading_configuration = ConfigurationServices.get_trading_configuration(
                    user=user, stock_id=stock_id
                )
                following_configuration = ConfigurationServices.get_following_configuration(
                    user=user, stock_id=stock_id
                )

                if trading_configuration is not None:
                    trading_configuration.delete()
                if following_configuration is not None:
                    following_configuration.delete()
                    
                overview_configuration.delete()

        else:
            overview_configuration.delete()

        return SuccessType.DELETE_SUCCESS, {}

    def check_is_overview_exist(user, stock_id):
        overview = ConfigurationTypeServices.get_overview()

        try:
            _ = Configuration.objects.get(
                user=user, config_type=overview.id, stock=stock_id)
            return True
        except Configuration.DoesNotExist:
            return False

    def get_overview_exist(user, stock_id):
        overview_type = ConfigurationTypeServices.get_overview()

        try:
            overview = Configuration.objects.get(
                user=user, config_type=overview_type.id, stock=stock_id)
            return overview
        except Configuration.DoesNotExist:
            return {}
        
    def get_all_overview(user):
        overview_type = ConfigurationTypeServices.get_overview()

        try:
            overview = Configuration.objects.get(
                user=user, config_type=overview_type.id)
            return overview
        except Configuration.DoesNotExist:
            return {}

    def handle_convert_data(template_data):
        stoploss_field_to_extract = ['stock_config_use_stop_loss_first_part', 'stock_config_percent_stop_loss_sell_first', 'stock_config_use_stop_loss_trigger',
                                     'stock_config_stop_loss_percent', 'stock_config_use_stop_loss_second_part', 'stock_config_percent_stop_loss_sell_second']
        takeprofit_field_to_extract = ['stock_config_use_take_profit_first_part', 'stock_config_percent_take_profit_sell_first', 'stock_config_use_take_profit_trigger',
                                       'stock_config_take_profit_percent', 'stock_config_use_take_profit_second_part', 'stock_config_percent_take_profit_sell_second']
        stoploss_obj = {field: template_data.get(
            field) for field in stoploss_field_to_extract}
        takeprofit_obj = {field: template_data.get(
            field) for field in takeprofit_field_to_extract}
        is_use_stoploss, percent_stoploss = calculate_stoploss(
            stoploss_obj=stoploss_obj)
        is_use_profit, percent_profit = calculate_profit(
            profit_obj=takeprofit_obj)
        percent_to_stoploss = round(
            1 - percent_stoploss, 2) if percent_stoploss <= 1 else 0
        percent_to_takeprofit = round(
            percent_profit - 1, 2) if percent_profit >= 1 else round(percent_profit, 2)
        percent_to_stoploss = percent_to_stoploss if is_use_stoploss else 0
        percent_to_takeprofit = percent_to_takeprofit if is_use_profit else 0

        return {
            'is_use_stoploss': is_use_stoploss,
            'percent_to_stoploss': percent_to_stoploss,
            'is_use_profit': is_use_profit,
            'percent_to_takeprofit': percent_to_takeprofit
        }

    @staticmethod
    def calculate_profit_using(configuration: Configuration):
        takeprofit_obj = {
            'stock_config_use_take_profit_first_part': configuration.stock_config_use_take_profit_first_part,
            'stock_config_percent_take_profit_sell_first': configuration.stock_config_percent_take_profit_sell_first,
            'stock_config_use_take_profit_trigger': configuration.stock_config_use_take_profit_trigger,
            'stock_config_take_profit_percent': configuration.stock_config_take_profit_percent,
            'stock_config_use_take_profit_second_part': configuration.stock_config_use_take_profit_second_part,
            'stock_config_percent_take_profit_sell_second': configuration.stock_config_percent_take_profit_sell_second
        }
        is_use_profit, percent_profit = calculate_profit(
            profit_obj=takeprofit_obj)

        return is_use_profit, percent_profit

    @staticmethod
    def calculate_stoploss_using(configuration: Configuration):
        stoploss_obj = {
            'stock_config_use_stop_loss_first_part': configuration.stock_config_use_stop_loss_first_part,
            'stock_config_percent_stop_loss_sell_first': configuration.stock_config_percent_stop_loss_sell_first,
            'stock_config_use_stop_loss_trigger': configuration.stock_config_use_stop_loss_trigger,
            'stock_config_stop_loss_percent': configuration.stock_config_stop_loss_percent,
            'stock_config_use_stop_loss_second_part': configuration.stock_config_use_stop_loss_second_part,
            'stock_config_percent_stop_loss_sell_second': configuration.stock_config_percent_stop_loss_sell_second
        }
        is_use_stl, percent_stl = calculate_stoploss(
            stoploss_obj=stoploss_obj)

        return is_use_stl, percent_stl
