from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.types import CommonTypeSerivce

from ...details.services import ConfigurationServices
from ...type.enums import ConfigurationTypeEnum

from ..serializers import ConfigurationSerializers
from ...candle.models import Candle
from ...type.models import ConfigurationType

from common.permissions.custom_permissions import ExchangeActionPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage

class ConfigurationStockDetailViews(APIView):
    def get(self, request):
        # user = request.user
        # stock_id = request.GET.get('stock_id')
        # config_type = request.GET.get('chart_type')
        if request.user.is_authenticated:
            user = request.user
            stock_id = request.GET.get('stock_id')
            config_type = request.GET.get('chart_type')
            data = ConfigurationServices.get_config_type_configuration(user=user, config_type=config_type, stock_id=stock_id)         
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Authentication required"}, status=401)        

    
    def put(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationServices.update_config_type_configuration(user=user, update_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationServices.update_config_type_configuration(user=user, update_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class ConfigurationAllStockDetailViews(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationServices.update_all_config_type_configuration(user=user, update_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)