
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from apps.authencation.role.models import Role
from apps.authencation.role.enums import UserRoleEnum
from common.api_key_validation import api_key_required
from common.permissions.custom_permissions import UpdateAccountUserByPassPermission
from apps.trading_limits.serializers import AccountTradingLimitsSerializer
from apps.trading_limits.services import AccountTradingLimitsServices
from apps.trading_limits.models import AccountTradingLimits
from ..exchange.services import ExchangeService
from .services import AccountService
from ..user_account.services import UserAccountService
from .serializers import AccountSerializer, SubAccountSerializer
from ..user_account.serializers import UserAccountSerializer
from .models import Account, AccountType, SubAccount
from .enums import AccountStatusEnum, AccountLoginStatusEnum
from apps.configuration.details.overview.services import ConfigurationOverviewServices
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage
from apps.trading.service.handlers import cancel_all_buy_orders, cancel_all_sell_orders
from apps import api
import hashlib
import logging
logger = logging.getLogger(__name__)


class AccountViews(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        user_accounts = UserAccountService.get_accounts_belong_user(
            user=user)
        account_ids = user_accounts.values_list('account', flat=True)
        accounts = Account.objects.filter(id__in=account_ids)
        account_data = []

        for account in accounts:
            trading_limits = AccountTradingLimitsServices.get_trading_limits_account(
                account_id=account.id)
            account_dict = {
                "id": account.id,
                "name": account.name,
                "password": account.password,
                "is_need_otp": account.is_need_otp,
                "exchange": account.exchange.code if account.exchange else None,
                "margin_account": None,
                "normal_account": None,
                "status": account.status,
                "login_status": account.login_status,
                "alias": account.alias,
                # "limits": trading_limits.limit
            }

            margin_account = SubAccount.objects.filter(
                main_account=account, account_type__name='Margin'
            ).first()

            if margin_account:
                account_dict["margin_account"] = {
                    "id": margin_account.id,
                    "name": margin_account.name,
                    "amount": margin_account.amount,
                    "balance": margin_account.balance,
                    "total_balance": margin_account.total_balance,
                    "valid": margin_account.valid
                }

            else:
                account_dict["margin_account"] = {
                    "valid": False
                }

            normal_account = SubAccount.objects.filter(
                main_account=account, account_type__name='Normal'
            ).first()
            if normal_account:
                account_dict["normal_account"] = {
                    "id": normal_account.id,
                    "name": normal_account.name,
                    "amount": normal_account.amount,
                    "balance": normal_account.balance,
                    "total_balance": normal_account.total_balance,
                    "valid": normal_account.valid
                }

            else:
                account_dict["normal_account"] = {
                    "valid": False
                }

            account_data.append(account_dict)

        return Response({
            'data': account_data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        body = request.data

        account_name = body.get('account_name')
        account_password = body.get('account_password')
        is_need_otp = body.get('is_need_otp')
        account_exchange = body.get('account_exchange')
        alias_name = body.get('account_alias_name')

        margin_account = body.get('margin_account')
        normal_account = body.get('normal_account')

        limits = body.get('limits')

        if account_name is None or account_password is None or is_need_otp is None:
            raise ValueError(ErrorMessages)

        if margin_account is None or normal_account is None:
            raise ValueError(ErrorMessages)

        is_exist_account = AccountService.check_account_exist_by_name(
            account_name=account_name)

        if is_exist_account:
            raise ValueError(ErrorMessages.ACCOUNT_IS_ALREADY_EXIST)

        exchange = ExchangeService.get_exchange_by_code(
            exchange_code=account_exchange)

        try:
            AccountService.validate_account_data_body(margin_account)
        except ValidationError as e:
            return Response({
                'errors': {'margin_account': str(e)}},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            AccountService.validate_account_data_body(normal_account)
        except ValidationError as e:
            return Response({
                'errors': {'normal_account': str(e)}},
                status=status.HTTP_400_BAD_REQUEST)

        hash_password = hashlib.md5(account_password.encode()).hexdigest()

        data = {
            'name': account_name,
            'password': hash_password,
            'is_need_otp': is_need_otp,
            'exchange': exchange.id,
            'status': AccountStatusEnum.Passive.value,
            'alias': alias_name,
            'login_status': AccountLoginStatusEnum.NotActive.value,
            'accounts': []
        }

        with transaction.atomic():
            account_serializer = AccountSerializer(data=data)
            if account_serializer.is_valid():
                account_instance = account_serializer.save()
                account_id = account_instance.id

                sub_accounts = []
                if margin_account is not None:
                    try:
                        if margin_account['valid'] == True:
                            margin_account_type = AccountService.get_account_type_by_name(
                                'Margin')
                            margin_account_data = {
                                'main_account': account_id,
                                'account_type': margin_account_type.id,
                                'name': AccountService.build_sub_account_naming('margin', account_name),
                                'amount': margin_account.get('amount'),
                                'balance': 0,
                                'total_balance': margin_account.get('total_balance')
                            }
                            sub_accounts.append(margin_account_data)
                    except ValidationError as e:
                        return Response({'errors': {'margin_account': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

                if normal_account is not None:
                    try:
                        if normal_account['valid'] == True:
                            normal_account_type = AccountService.get_account_type_by_name(
                                'Normal')
                            normal_account_data = {
                                'main_account': account_id,
                                'account_type': normal_account_type.id,
                                'name': AccountService.build_sub_account_naming('normal', account_name),
                                'amount': normal_account.get('amount'),
                                'balance': 0,
                                'total_balance': normal_account.get('total_balance')
                            }
                            sub_accounts.append(normal_account_data)
                    except ValidationError as e:
                        return Response({'errors': {'normal_account': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

                for sub_account_data in sub_accounts:
                    sub_account_serializer = SubAccountSerializer(
                        data=sub_account_data)
                    if sub_account_serializer.is_valid():
                        data['accounts'].append(sub_account_data)
                        sub_account_serializer.save()
                    else:
                        return Response({
                            'errors': {
                                'message': f'sub_account table {str(sub_account_serializer.errors)}'
                            }
                        }, status=status.HTTP_400_BAD_REQUEST)

                # init the trading_limit
                limits = 100 if limits is None else int(limits)
                limit_init_data = {
                    "account": account_id,
                    "limit": limits
                }
                trading_limits_serializer = AccountTradingLimitsSerializer(
                    data=limit_init_data)
                if trading_limits_serializer.is_valid():
                    trading_limits_serializer.save()
                else:
                    return Response({
                        'errors': {
                            'message': f'trading_limits table {str(trading_limits_serializer.errors)}'
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)
                # init the user_account
                user_account_data = {
                    'user': user.id,
                    'account': account_id
                }
                user_account_serializer = UserAccountSerializer(
                    data=user_account_data)
                if user_account_serializer.is_valid():
                    user_account_serializer.save()
                    data['limits'] = limits

                    return Response({'data': data}, status=status.HTTP_201_CREATED)

                else:
                    return Response({
                        'errors': {
                            'message': f'user_account table {str(user_account_serializer.errors)}'
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'errors': {
                    'message': str(account_serializer.errors)
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = request.user
        body = request.data

        account_id = body.get('account_id')
        account_password = body.get('account_password')
        is_need_otp = body.get('is_need_otp')
        account_alias_name = body.get('account_alias_name')
        trading_limits = body.get('limits')
        margin_account = body.get('margin_account')
        normal_account = body.get('normal_account')

        # Fetch the account
        account = AccountService.get_account_by_id(account_id=account_id)
        if trading_limits:
            account_trading_limits = AccountTradingLimitsServices.get_trading_limits_account(
                account_id=account.id)

        if not account or (trading_limits and not account_trading_limits):
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the account belongs to the user
        is_account_belong_user = UserAccountService.check_account_belong_user(
            user=user, account=account)
        if not is_account_belong_user:
            return Response({'error': 'User does not have access to this account'}, status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():

                # Handle updating margin_account if present
                if margin_account is not None:
                    margin_validation = AccountService.validate_account_data_partial_body(
                        margin_account)
                    if margin_validation:
                        margin_account_instance = SubAccount.objects.filter(
                            main_account_id=account_id, account_type__name='Margin'
                        ).first()

                        if margin_account_instance:
                            margin_serializer = SubAccountSerializer(
                                margin_account_instance, data=margin_account, partial=True)
                            if not margin_serializer.is_valid():
                                raise ValueError("Invalid margin account data")
                            data = margin_serializer.save()
                        else:
                            raise ValueError("Margin account does not exist")

                # Handle updating normal_account if present
                if normal_account is not None:
                    normal_validation = AccountService.validate_account_data_partial_body(
                        normal_account)
                    if normal_validation:
                        normal_account_instance = SubAccount.objects.filter(
                            main_account_id=account_id, account_type__name='Normal'
                        ).first()

                        if normal_account_instance:
                            normal_serializer = SubAccountSerializer(
                                normal_account_instance, data=normal_account, partial=True)
                            if not normal_serializer.is_valid():
                                raise ValueError("Invalid normal account data")
                            normal_serializer.save()
                        else:
                            raise ValueError("Normal account does not exist")

                # Prepare data for updating
                data = {}
                if account_password is not None:
                    data['password'] = hashlib.md5(
                        account_password.encode()).hexdigest()
                if is_need_otp is not None:
                    data['is_need_otp'] = is_need_otp
                if account_alias_name is not None:
                    data['alias'] = account_alias_name

                # Update the account instance
                serializer = AccountSerializer(
                    account, data=data, partial=True)

                # Handle updating trading limits if present
                trading_limits_serializer = None
                if trading_limits is not None:
                    trading_limits_serializer = AccountTradingLimitsSerializer(
                        account_trading_limits, data={"limit": trading_limits}, partial=True)

                if serializer.is_valid() and (trading_limits is None or (trading_limits_serializer and trading_limits_serializer.is_valid())):
                    serializer.save()
                    if trading_limits_serializer:
                        trading_limits_serializer.save()
                    return_data = serializer.data
                    if 'exchange' in return_data:
                        return_data['exchange'] = ExchangeService.get_exchange_by_id(
                            exchange_id=return_data['exchange']).code
                    if trading_limits is not None:
                        return_data['limits'] = trading_limits
                    return Response({
                        'data': {
                            'message': 'Update succesfully!'
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    errors = serializer.errors
                    if trading_limits_serializer and not trading_limits_serializer.is_valid():
                        errors.update(trading_limits_serializer.errors)
                    return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

        except (IntegrityError, ValueError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        body = request.data

        account_id = body.get('account_id')

        # Fetch the account
        account = AccountService.get_account_by_id(account_id=account_id)
        if not account:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check the limits row created
        trading_limits = AccountTradingLimitsServices.get_trading_limits_account(
            account_id=account.id)
        if not trading_limits:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the account belongs to the user
        account_belong_user = UserAccountService.get_account_belong_user(
            user=user, account=account)
        if not account_belong_user:
            return Response({'error': 'User does not have access to this account'}, status=status.HTTP_403_FORBIDDEN)

        # Perform the deletion within a transaction
        with transaction.atomic():
            SubAccount.objects.filter(main_account=account).delete()
            account.delete()
            account_belong_user.delete()
            trading_limits.delete()

            return Response({
                'data': {
                    'message': SuccessMessage.DELETE_ACCOUNT_SUCCESSFUL
                }
            }, status=status.HTTP_204_NO_CONTENT)

class AccountTradingView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user            
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            is_block_buy = vps_account.is_block_buy
            is_block_sell = vps_account.is_block_sell
            return Response({
                        "data": {
                            "is_block_buy": is_block_buy,
                            "is_block_sell": is_block_sell
                        }
                    })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        try:
            user = request.user
            body = request.data
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            url = api.TRADING_URL
            is_block_buy = body["is_block_buy"]
            is_block_sell = body["is_block_sell"]
            type_block = body["type"]
            # Hủy lệnh mua hoặc bán khi block buy hoặc block sell
            # if is_block_buy:
            #     logger.info(f'Bắt đầu chạy cancel_all_buy_orders khi block buy')
            #     cancel_all_buy_orders(user, account_name, account_num, 'all_order', api.TRADING_URL, session_id, '', "B")
            #     logger.info(f'Đã chạy xong cancel_all_buy_orders khi block buy')
            # if is_block_sell:
            #     logger.info(f'Bắt đầu chạy cancel_all_sell_orders khi block sell')
            #     cancel_all_sell_orders(user, account_name, account_num, 'all_order', api.TRADING_URL, session_id, '', "S")
            #     logger.info(f'Đã chạy xong cancel_all_sell_orders khi block sell')
            vps_data_update = {
                "is_block_buy": is_block_buy,
                "is_block_sell": is_block_sell,
                "login_status": AccountLoginStatusEnum.LoginSuccess.value,
                "status": AccountStatusEnum.Active.value
            }
            vps_serializer = AccountSerializer(vps_account, data=vps_data_update, partial=True)
            if vps_serializer.is_valid():
                vps_serializer.save()
            overview_configuration = ConfigurationOverviewServices.update_block_trade_overview(user=user, type_block=type_block, is_block_buy=is_block_buy, is_block_sell=is_block_sell )   

            if overview_configuration:
                return Response({
                    "data": {
                        "is_block_buy": is_block_buy,
                        "is_block_sell": is_block_sell,
                        "status": 'sussces',
                    }
                })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            account_id = request.GET.get('id')

            if not account_id:
                return Response({"error": "ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        trading_limits = AccountTradingLimitsServices.get_trading_limits_account(
            account_id=account.id)

        account_data = {
            "id": account.id,
            "name": account.name,
            "password": account.password,
            "is_need_otp": account.is_need_otp,
            "exchange": account.exchange.code if account.exchange else None,
            "margin_account": None,
            "normal_account": None,
            "status": account.status,
            "login_status": account.login_status,
            "alias": account.alias,
            "limits": trading_limits.limit
        }

        margin_account = SubAccount.objects.filter(
            main_account=account, account_type__name='Margin'
        ).first()
        if margin_account:
            account_data["margin_account"] = {
                "valid": margin_account.valid,
                "name": margin_account.name,
                "amount": margin_account.amount,
                "balance": margin_account.balance,
                "total_balance": margin_account.total_balance
            }

        normal_account = SubAccount.objects.filter(
            main_account=account, account_type__name='Normal'
        ).first()
        if normal_account:
            account_data["normal_account"] = {
                "valid": normal_account.valid,
                "name": normal_account.name,
                "amount": normal_account.amount,
                "balance": normal_account.balance,
                "total_balance": normal_account.total_balance
            }

        return Response({
            'data': account_data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user = request.user
            body = request.data

            account_type = body.get('type')
            main_account_id = body.get('main_account')
            amount = body.get('amount')

            if account_type not in ['margin', 'normal']:
                return Response({"error": "Invalid account type"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                main_account = AccountService.get_account_by_id(
                    account_id=main_account_id)
            except Account.DoesNotExist:
                return Response({"error": "Main account not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user owns the account
            is_account_belong_user = UserAccountService.get_account_belong_user(
                user=user, account=main_account.id)
            if not is_account_belong_user:
                return Response({"error": "User does not own this account"}, status=status.HTTP_403_FORBIDDEN)

            account_type_name = 'Margin' if account_type == 'margin' else 'Normal'
            existing_subaccount = SubAccount.objects.filter(
                main_account=main_account, account_type__name=account_type_name
            ).first()

            if existing_subaccount:
                return Response({
                    'data': {
                        'message': 'SubAccount already exists',
                        'subaccount': {
                            'valid': existing_subaccount.valid,
                            'name': existing_subaccount.name,
                            'amount': existing_subaccount.amount,
                            'balance': existing_subaccount.balance,
                            'total_balance': existing_subaccount.total_balance
                        }
                    }
                }, status=status.HTTP_200_OK)

            new_subaccount = SubAccount(
                main_account=main_account,
                account_type=AccountType.objects.get(name=account_type_name),
                name=f"{account_type_name} Account",
                amount=amount,
                balance=amount
            )
            new_subaccount.save()

            return Response({
                'data': {
                    'message': 'SubAccount created successfully',
                    'subaccount': {
                        'valid': new_subaccount.valid,
                        'name': new_subaccount.name,
                        'amount': new_subaccount.amount,
                        'balance': new_subaccount.balance,
                        'total_balance': new_subaccount.total_balance
                    }
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({
                'data': str(error)
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            user = request.user
            body = request.data

            account_type = body.get('type')
            main_account_id = body.get('main_account')
            amount = body.get('amount')
            use = body.get('use')

            if account_type not in ['margin', 'normal']:
                return Response({"error": "Invalid account type"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                main_account = AccountService.get_account_by_id(
                    account_id=main_account_id)
            except Account.DoesNotExist:
                return Response({"error": "Main account not found"}, status=status.HTTP_404_NOT_FOUND)

                # Check if user owns the account
            is_account_belong_user = UserAccountService.get_account_belong_user(
                user=user, account=main_account.id)
            if not is_account_belong_user:
                return Response({"error": "User does not own this account"}, status=status.HTTP_403_FORBIDDEN)

            account_type_name = 'Margin' if account_type == 'margin' else 'Normal'
            subaccount = SubAccount.objects.filter(
                main_account=main_account, account_type__name=account_type_name
            ).first()

            if not subaccount:
                return Response({"error": "SubAccount not found"}, status=status.HTTP_404_NOT_FOUND)

            if subaccount.total_balance < subaccount.amount + amount or subaccount.amount + amount < 0 or subaccount.balance + amount < 0:
                return Response({"error": "Cannot update the amount"}, status=status.HTTP_400_BAD_REQUEST)

            subaccount.amount += amount
            subaccount.balance += amount
            subaccount.save()

            return Response({
                'data': {
                    'message': 'SubAccount updated successfully',
                    'subaccount': {
                        'valid': subaccount.valid,
                        'name': subaccount.name,
                        'amount': subaccount.amount,
                        'balance': subaccount.balance,
                        'total_balance': subaccount.total_balance
                    }
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                'data': str(error)
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            user = request.user
            body = request.data

            account_type = body.get('type')
            main_account_id = body.get('main_account')

            if account_type not in ['margin', 'normal']:
                return Response({"error": "Invalid account type"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                main_account = AccountService.get_account_by_id(
                    account_id=main_account_id)
            except Account.DoesNotExist:
                return Response({"error": "Main account not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user owns the account
            is_account_belong_user = UserAccountService.get_account_belong_user(
                user=user, account=main_account.id)
            if not is_account_belong_user:
                return Response({"error": "User does not own this account"}, status=status.HTTP_403_FORBIDDEN)

            account_type_name = 'Margin' if account_type == 'margin' else 'Normal'
            other_account_type_name = 'Margin' if account_type == 'normal' else 'Normal'
            subaccount = SubAccount.objects.filter(
                main_account=main_account, account_type__name=account_type_name
            ).first()

            if not subaccount:
                return Response({"error": "SubAccount not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if it's the only subaccount of its type
            other_subaccount_exists = SubAccount.objects.filter(
                main_account=main_account, account_type__name=other_account_type_name
            ).exists()

            if not other_subaccount_exists:
                return Response({"error": "Cannot delete the only SubAccount of this type"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the subaccount
            subaccount.delete()

            return Response({
                'data': {
                    'message': 'SubAccount deleted successfully'
                }
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response({
                'data': str(error)
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([UpdateAccountUserByPassPermission])
def put_admin(requests):
    user = requests.user
    body = requests.data

    vps_account = body.get("account")
    vps_request_verify_token = body.get("vps_request_verify_token")
    vps_cookie = body.get("vps_cookie")
    login_status = body.get("login_status")

    account = AccountService.get_account_by_name(account_name=vps_account)

    vps_update_data = {
        "vps_request_verify_token": vps_request_verify_token,
        "vps_cookie": vps_cookie
    }

    if login_status:
        vps_update_data["login_status"] = login_status

    serializer = AccountSerializer(account, data=vps_update_data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'data': {
                "message": "Update is successfully"
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': {
                'message': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
