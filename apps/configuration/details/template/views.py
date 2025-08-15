from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.types import CommonTypeSerivce
from .services import ConfigurationTemplateServices
from ..serializers import ConfigurationSerializers
from ...candle.models import Candle
from ...type.models import ConfigurationType

from common.permissions.custom_permissions import ExchangeActionPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage

class ConfigurationTemplateViews(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        data = ConfigurationTemplateServices.get_configuration_template(user=user)
        return Response(data, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationTemplateServices.create_configuration_template(user=user,template_data=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_TEMPLATE_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)   
         
    def put(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationTemplateServices.update_configuration_template(user=user, template_data_update=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_TEMPLATE_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)


#Tạm thời thêm để update cấu hình tổng quát
class ConfigurationTemplateUpdate(APIView):
    serializers = ConfigurationSerializers
    permission_classes = [IsAuthenticated]
  
    def post(self, request):
        user = request.user
        data = request.data
        
        res_type, res_data = ConfigurationTemplateServices.update_configuration_template(user=user, template_data_update=data)
        
        if CommonTypeSerivce.check_response_type(res_type=res_type):
            return Response({'data': res_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'message': ErrorMessages.UPDATE_CONFIGURATION_TEMPLATE_FAILED}}, status=status.HTTP_406_NOT_ACCEPTABLE)