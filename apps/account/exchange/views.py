from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Exchange
from .serializers import ExchangeSerializer
from .services import ExchangeService

from common.permissions.custom_permissions import ExchangeActionPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage


class ExchangeViews(APIView):
    serializers = ExchangeSerializer
    permission_classes = [ExchangeActionPermission]
    
    def get(self, request):
        exchanges = ExchangeService.get_exchanges()
        serializer = ExchangeSerializer(exchanges, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExchangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        exchange_code = request.data.get('code')
        exchange = ExchangeService.get_exchange_by_code(exchange_code=exchange_code)
        serializer = ExchangeSerializer(exchange, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        exchange_code = request.data.get('code')
        
        if exchange_code == 'VPS':
            return Response({'errors': ErrorMessages.VPS_DELETE_ERRO}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            exchange = ExchangeService.get_exchange_by_code(exchange_code=exchange_code)
            exchange.delete()
            return Response({'data': {'message': SuccessMessage.DELETE_ROLE_SUCCESSFUL}},status=status.HTTP_204_NO_CONTENT)
        except (Exchange.DoesNotExist):
            raise ValueError(ErrorMessages.ROLE_DOES_NOT_EXIST)
        