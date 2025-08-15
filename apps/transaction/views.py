import django.db
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from apps.configuration.details.overview.services import ConfigurationOverviewServices
from apps.account.detail.models import Account
from apps.account.detail.services import AccountService
from apps.stock.services import StockService
from apps.account.user_account.services import UserAccountService
from .models import TransactionLog
from .serializers import TransactionLogSerializer


class TransactionLogViews(APIView):
    serializer_class = TransactionLogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        overview_configuration = ConfigurationOverviewServices.get_detail_stock_configurations(user=user)
        
        transaction_logs = []
        
        for configuration in overview_configuration:
            stock = configuration.get('stock_id')
            transactions = TransactionLog.objects.filter(
                    user=user, stock=stock)

            for transaction in transactions:
                    account = transaction.account
                    _data = {
                        'vps_account_name': account.name,
                        'stock': configuration.get('stock_name'),
                        'pid_type': transaction.signal_type,
                        'price_pid': transaction.price,
                        'fee_pid': transaction.fee,
                        'created_at': str(transaction.created_at),
                        'volume_set': transaction.volume_set,
                        'volume_match': transaction.volume_match
                    }
                    transaction_logs.append(_data)
                    
        sorted_transactions_log = sorted(
                transaction_logs, key=lambda x: x['created_at'], reverse=True)
            
        return Response({'data': sorted_transactions_log}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        body = request.data

        for idx, data in enumerate(body):
                required_fields = ['vps_account_name', 'stock', 'pid_type',
                                   'price_pid', 'fee_pid', 'create_at', 'volume_set', 'volume_match']

                if data['pid_type'] not in ['buy', 'sell']:
                    continue

                data_fileds = data.keys()

                if sorted(required_fields) != sorted(data_fileds):
                    return Response({'error': {'message': 'Please to provide enough fields!', 'postions': f'Item in the {idx}'}}, status=status.HTTP_400_BAD_REQUEST)

                account_name = data.get('vps_account_name')
                stock_symbol = data.get('stock')
                signal_type = data.get('pid_type')
                price_pid = data.get('price_pid')
                fee_pid = data.get('fee_pid')
                create_at = data.get('create_at')
                volume_set = data.get('volume_set')
                volume_match = data.get('volume_match')

                account = AccountService.get_account_by_name(account_name=account_name)
                stock = StockService.get_stock_by_symbol(stock_symbol=stock_symbol)
                _ = UserAccountService.check_account_belong_user(user=user, account=account.id)

                init_data = {
                    'user': user.id,
                    'account': account.id,
                    'stock': stock.id,
                    'signal_type': signal_type,
                    'price': price_pid,
                    'fee': fee_pid,
                    'created_at': datetime.strptime(create_at, "%d/%m/%Y %H:%M:%S"),
                    'volume_set': volume_set,
                    'volume_match': volume_match
                }

                serializers = TransactionLogSerializer(data=init_data)

                if serializers.is_valid():
                    serializers.save()
                else:
                    return Response({'error': {'message': f'{serializers.error_messages}', 'postions': f'Item in the {idx}'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': {'message': 'Create transaction logs successfully!'}}, status=status.HTTP_201_CREATED)
