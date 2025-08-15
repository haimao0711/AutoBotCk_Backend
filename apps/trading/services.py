from common.errors.messages import ErrorMessages
from django.utils import timezone
from datetime import timedelta

from apps.trading.enum.enums import StatusPidEnum
from .models import Trading
from .serializers import TradingSerializer


class TradingService:

    @staticmethod
    def update_trading_status(trading_instance: Trading, new_status: str) -> dict:
        valid_statuses = dict(Trading._STATUS_CHOICES)

        if new_status not in valid_statuses:
            return {'error': 'Invalid status provided'}

        current_status = trading_instance.trading_status
        now = timezone.now()

        if current_status == 'completed':
            if new_status == 'waiting_to_sell' and (now > trading_instance.last_status_change + timedelta(days=2)):
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from completed'}

        elif current_status == 'selling_processing':
            if new_status == 'ready_to_buy' and (now > trading_instance.last_status_change + timedelta(days=1)):
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from selling_processing'}

        elif current_status == 'waiting_to_sell':
            if new_status == 'ready_to_sell' and (now > trading_instance.last_status_change + timedelta(days=2)):
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from waiting_to_sell'}

        elif current_status == 'ready_to_sell':
            if new_status == 'selling_processing':
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from ready_to_sell'}

        elif current_status == 'buying_processing':
            if new_status == 'waiting_to_buy':
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from buying_processing'}

        elif current_status == 'ready_to_buy':
            if new_status == 'buying_processing':
                trading_instance.trading_status = new_status
            else:
                return {'error': 'Cannot transition to the requested status from ready_to_buy'}

        trading_instance.last_status_change = now
        trading_instance.save()

        return {'success': f'Status updated to {new_status}'}

    @staticmethod
    def calculate_volume(data_volumes):
        total = 0
        return_obj = {}
        for key, value in data_volumes.items():
            total += value.get('volume')

        for key, value in data_volumes.items():
            if total == 0:
                return_obj[key] = 0
            else:
                return_obj[key] = value.get('volume')/total

        return return_obj

    @staticmethod
    def get_trading_by_id_base_configuration(base_id):
        try:
            trading = Trading.objects.get(base_configuration=base_id)
            return TradingSerializer(instance=trading).data
        except Exception as error:
            base_data = {
                'base_configuration': base_id,
                'status_pid': StatusPidEnum.FOLLOW,
                'max_volume_buy': 0,
                'volume_buy': 0,
                'volume_sell': 0,
                'aver_price_buy': 0,
                'profit': 0,
            }
            return base_data
        
    @staticmethod
    def get_trading_data_bulk(configuration_ids):
        """
        Lấy dữ liệu giao dịch hàng loạt dựa trên danh sách base_configuration ID.
        :param configuration_ids: List các ID của base_configuration.
        :return: Dictionary với key là base_id và value là dữ liệu trading tương ứng.
        """
        try:
            # Truy vấn tất cả các bản ghi Trading liên quan đến configuration_ids
            tradings = Trading.objects.filter(base_configuration__in=configuration_ids)
            serialized_data = TradingSerializer(instance=tradings, many=True).data

            # Tạo map base_id -> trading_data
            trading_data_map = {item['base_configuration']: item for item in serialized_data}

            # Lấp đầy dữ liệu mặc định cho các ID không tìm thấy
            for base_id in configuration_ids:
                if base_id not in trading_data_map:
                    trading_data_map[base_id] = {
                        'base_configuration': base_id,
                        'status_pid': StatusPidEnum.FOLLOW,
                        'max_volume_buy': 0,
                        'volume_buy': 0,
                        'volume_sell': 0,
                        'aver_price_buy': 0,
                        'profit': 0,
                    }

            return trading_data_map

        except Exception as error:
            print(f"Error in get_trading_data_bulk: {str(error)}")
            # Trả về dữ liệu mặc định nếu có lỗi
            return {
                base_id: {
                    'base_configuration': base_id,
                    'status_pid': StatusPidEnum.FOLLOW,
                    'max_volume_buy': 0,
                    'volume_buy': 0,
                    'volume_sell': 0,
                    'aver_price_buy': 0,
                    'profit': 0,
                }
                for base_id in configuration_ids
            }


    @staticmethod
    def initializer(data):
        if TradingService.check_is_exist(data.get('base_configuration')):
            return
        data['trading_status'] = 'ready_to_buy'
        trading_serializer = TradingSerializer(data=data)
        if trading_serializer.is_valid():
            trading_serializer.save()
        else:
            return

    @staticmethod
    def check_is_exist(base_configuration_id):
        try:
            _ = Trading.objects.get(base_configuration=base_configuration_id)
            return True
        except Trading.DoesNotExist as error:
            return False

    @staticmethod
    def update_max_volume_buy(base_configuration_id, max_volume_buy):
        try:
            Trading.objects.filter(base_configuration_id=base_configuration_id).update(
                max_volume_buy=max_volume_buy)
            return True, "Max volume buy updated successfully."
        except Exception as e:
            return False, f"Error updating max volume buy: {str(e)}"

    @staticmethod
    def update_base_configuration_ids(base_configuration_ids, data_updated):
        for base_configuration_id in base_configuration_ids:
            TradingService.update_max_volume_buy(
                base_configuration_id, data_updated[base_configuration_id])
