from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from common.api_key_validation import api_key_required
from apps.account.detail.models import Account
from apps.account.user_account.models import UserAccount


@api_view(['POST'])
@api_key_required
def bot_request_otp(request):
    account_vps_name = request.data.get('account_vps_name')
    user = request.user
    try:
        vps = Account.objects.get(name=account_vps_name)
        _ = UserAccount.objects.get(account=vps, user=user)
        cache_key = f'{account_vps_name}-request-otp'
        cache.set(cache_key, True, timeout=120)
        return Response(status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)
    except UserAccount.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@api_key_required
def bot_get_otp(request):
    account_vps_name = request.GET.get('account_vps_name')
    user = request.user
    try:
        vps = Account.objects.get(name=account_vps_name)
        _ = UserAccount.objects.get(account=vps, user=user)
        cache_key = f'{account_vps_name}-otp'
        otp = cache.get(cache_key)
        if otp is not None:
            return Response({'data': {'otp': otp}}, status=status.HTTP_200_OK)
        return Response({'error': {'message': 'OPT is not valid now', 'otp': ''}}, status=status.HTTP_204_NO_CONTENT)
    except Account.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)
    except UserAccount.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_status_bot_request_otp(request):
    user = request.user
    account_vpses = UserAccount.objects.filter(user=user)
    result = []
    for account in account_vpses:
        object = {}
        vps = account.account
        object['account'] = vps.name
        otp = cache.get(
            f'{vps.name}-request-otp')
        if otp is not None:
            object['request_status'] = otp
        else:
            object['request_status'] = False
        result.append(object)
    return Response({'data': result}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_otp(request):
    user = request.user
    account_vps_id = request.data.get('account_vps_id')
    otp = request.data.get('otp')
    try:
        vps = Account.objects.get(id=account_vps_id)
        account = UserAccount.objects.get(
            user=user, account=vps)
        account_vps_name = account.account.name
        cache.set(f'{account_vps_name}-otp', otp, timeout=60)
        cache.set(f'{account_vps_name}-request-otp', False)
        return Response({'data': {'message': 'Send OTP is succesfully'}}, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)
    except UserAccount.DoesNotExist:
        return Response({'error': {'message': 'Cannot find the account vps'}}, status=status.HTTP_404_NOT_FOUND)
