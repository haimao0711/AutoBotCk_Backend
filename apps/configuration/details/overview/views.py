import apps.trading.service
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.success.types import SuccessType
from common.errors.types import ErrorType

from apps.account.detail.services import AccountService
from .services import ConfigurationOverviewServices
from ..serializers import ConfigurationSerializers
from ...candle.models import Candle
from ...type.models import ConfigurationType

from apps.trading.views import TradingViews, active_trading_threads  
from common.types import CommonTypeSerivce
from common.permissions.custom_permissions import ExchangeActionPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage


from datetime import datetime

class ConfigurationOverviewViews(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        data = ConfigurationOverviewServices.get_detail_stock_configurations(user=user)
        return Response(data, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        user = request.user
        data = request.data
       
        res_type, res_data = ConfigurationOverviewServices.create_overview_configuration(user=user,init_overview_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_OVERVIEW_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)   
         
    def put(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationOverviewServices.update_overview_configuration(user=user, update_overview_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': res_data}, status=status.HTTP_406_NOT_ACCEPTABLE)

#Tạm thời thêm class để đổi put thành post
class ConfigurationOverviewUpdate(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        print('check request update data: ', data)
        res_type, res_data = ConfigurationOverviewServices.update_overview_configuration(user=user, update_overview_data=data)
      
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': res_data}, status=status.HTTP_406_NOT_ACCEPTABLE)

#Tạm thời thêm class để đổi delete thành post
class ConfigurationOverviewDelete(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationOverviewServices.delete_overview_configuration(user=user, delete_overview_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.DELETE_CONFIGURATION_OVERVIEW_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)

class ConfigurationOverviewBalance(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        data = ConfigurationOverviewServices.get_stock_balance(user=user)
        return Response(data, status=status.HTTP_200_OK)


class ConfigurationOverviewRequestViews(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]

    def request_buy(self, request):
        try:
            user = request.user
            symbol = request.data.get('stock_name')
            stock_id = request.data.get('stock_id')
            is_use_chart_action = request.data.get('is_use_chart_action')
            data_update = {
                'stock_id': request.data.get('stock_id'),
                'is_buy_hand': request.data.get('is_buy_hand'),
                'is_sell_hand': request.data.get('is_sell_hand')
            }       
            is_trading_request = TradingViews.request_trading(user, stock_id=stock_id, symbol=symbol, request_buy=True, request_sell=False, volume_sell='', is_use_chart_action=is_use_chart_action)
            if is_trading_request:
                status_code, response_data = ConfigurationOverviewServices.update_a_overview_configuration(
                    user=user,
                    update_overview_data=data_update
                )
                if status_code == SuccessType.UPDATED_SUCCESS:
                    return Response(
                        {"data": response_data},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Cập nhật thất bại", "details": response_data},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
                return Response(
                    {"data": {"message": "Yêu cầu mua không thành công"}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")
            ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
            return Response({"error": str(e)}, status=500)



    def request_sell(self, request):
        try:
            user = request.user
            symbol = request.data.get('stock_name')
            stock_id = request.data.get('stock_id')
            volume_sell = request.data.get('volume_sell')
            is_use_chart_action = request.data.get('is_use_chart_action')
            data_update = {
                'stock_id': request.data.get('stock_id'),
                'is_buy_hand': request.data.get('is_buy_hand'),
                'is_sell_hand': request.data.get('is_sell_hand')
            }
            is_trading_request = TradingViews.request_trading(user, stock_id=stock_id, symbol=symbol, request_buy=False, request_sell=True, volume_sell=volume_sell, is_use_chart_action=is_use_chart_action)
            if is_trading_request:
                status_code, response_data = ConfigurationOverviewServices.update_a_overview_configuration(
                    user=user,
                    update_overview_data=data_update
                )
                if status_code == SuccessType.UPDATED_SUCCESS:
                    return Response(
                        {"data": response_data},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Cập nhật thất bại", "details": response_data},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
                return Response(
                    {"data": {"message": "Yêu cầu bán không thành công"}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")
            ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
            return Response({"error": str(e)}, status=500)
    
    def stop_request(self, request):
        try:
            user = request.user
            symbol = request.data.get('stock_name')
            stock_id = request.data.get('stock_id')
            ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
            TradingViews.cancel_request_oder(user, symbol)
            return Response(
                        {"data": {"message": "Dừng mua bán tay thành công"}},
                        status=status.HTTP_200_OK
                    )
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")
            ConfigurationOverviewRequestViews.stop_request_trade(user, stock_id)
            return Response({"error": str(e)}, status=500)

    def post(self,request):
        if request.path.endswith('/request-stoptrade'):
            return self.stop_request(request)
        elif request.path.endswith('/request-buy'):
            return self.request_buy(request)
        elif request.path.endswith('/request-sell'):
            return self.request_sell(request)
    
    @staticmethod
    def stop_request_trade(user, stock_id):
        try:
            # Dừng yêu cầu giao dịch, cập nhật trạng thái
            data_update = {
                'stock_id': stock_id,
                'is_buy_hand': False,
                'is_sell_hand': False
            }

            # Cập nhật thông tin trong database hoặc hệ thống
            status_code, response_data = ConfigurationOverviewServices.update_a_overview_configuration(
                user=user,
                update_overview_data=data_update
            )
            
            if status_code == SuccessType.UPDATED_SUCCESS:
                print(f"stop_request_trade: Yêu cầu { 'mua bán tay' } cho {stock_id} đã được dừng.")
            else:
                print(f"stop_request_trade: Không thể cập nhật trạng thái dừng giao dịch cho {stock_id}.")

            # Kiểm tra và dừng tiến trình nếu có
            key = f"{user.id}_{stock_id}"
            if key in active_trading_threads:
                stop_event = active_trading_threads[key]['stop_event']
                stop_event.set()  # Gửi tín hiệu dừng tiến trình
                active_trading_threads[key]['thread'].join()  # Đợi cho đến khi tiến trình dừng hoàn toàn
                del active_trading_threads[key]  # Xóa tiến trình khỏi danh sách
                print(f"Đã dừng tiến trình giao dịch cho {stock_id} của người dùng {user.id}.")
            else:
                print(f"Không tìm thấy tiến trình giao dịch cho {stock_id} của người dùng {user.id}.")

        except Exception as e:
            print(f"Lỗi trong quá trình dừng giao dịch: {e}")