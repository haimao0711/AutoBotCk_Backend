from datetime import datetime
import time as t
import pytz

from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.account.user_account.services import UserAccountService
from apps.account.detail.serializers import AccountSerializer
from apps.account.detail.models import Account
from apps.account.detail.enums import AccountLoginStatusEnum, AccountStatusEnum
from apps.account.detail.services import AccountService
from apps.authencation_exchange.service.smartOne.login import login_smartone_vps, login_get_session_vps_step_1, login_get_session_vps_step_2
from apps.authencation_exchange.service.enums import LoginStatusEnum
from apps.telegram.sender import send_message
from common.signal.enums import SignalTelegramEnum
from apps.telegram.enum.enums import MessageTypeEnum
from common.api.smartone.handler import validate_session
from apps.trading.service.handlers import cancel_all_orders
from apps.trading.scheduler.celery_scheduler import create_user_schedules, remove_user_schedules
from apps.configuration.details.overview.services import ConfigurationOverviewServices
from common.errors.messages import ErrorMessages
from apps import api

class AuthencationStockExchagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        body = request.data

        # Lấy dữ liệu từ request
        otp = body.get("otp")
        is_trading = body.get("isTrading")
        vps_account = AccountService.get_account_by_user(user)
        
        if not vps_account:
            return Response({"data": {"message": ErrorMessages.ACCOUNT_DOES_NOT_EXIST, "status": 0}}, status=HTTP_400_BAD_REQUEST)

        account_name = vps_account.name
        account_num = vps_account.account_num
        pass_login = vps_account.password
        url = api.TRADING_URL
        session_id_old = vps_account.vps_session_id
        session_id = session_id_old if session_id_old else 'stop_trading'
        list_accounts = Account.objects.filter(name=account_name)
        # Hàm cập nhật dữ liệu VPS
        def update_vps_data(session_id, message, status):
            for vps_account in list_accounts:
                vps_data_update = {
                    "vps_session_id": session_id,
                    "login_status": AccountLoginStatusEnum.LoginSuccess.value,
                    "status": AccountStatusEnum.Active.value
                }
                vps_serializer = AccountSerializer(vps_account, data=vps_data_update, partial=True)
                if vps_serializer.is_valid():
                    vps_serializer.save()

            return {
                "message": message,
                "status": status,
                "session_id": session_id
            }
        # Kiểm tra xem có đang giao dịch không
        if is_trading:
            cancel_all_orders(user, account_name, account_num, '', url, session_id, '', 'All')
            result = update_vps_data(session_id, "Trading is stopped!", 2)
            remove_user_schedules(user)  # Dừng scheduler của user (xóa PeriodicTask trong DB)
            ConfigurationOverviewServices.restart_request_trade_overview(user) # Reset is_trading và mua/bán tay
            user.scheduler_status = False
            user.save()
        else:
            # Đăng nhập để lấy session mới
            session_login_1 = login_get_session_vps_step_1(account_name, pass_login)
            session_login_2 = None
            if session_login_1:
                session_login_2 = login_get_session_vps_step_2(account_name, pass_login, otp)
            else:
                return Response({"data": {"message": "Tài khoản hoặc mật khẩu VPS chưa đúng. Vui lòng cập nhật lại mật khẩu VPS!", "status": 0}}, status=HTTP_400_BAD_REQUEST)
            if session_login_2:
                session_id = session_login_2

            # Nếu session thay đổi, hủy tất cả lệnh cũ và reset trạng thái
            if session_id != session_id_old:
                cancel_all_orders(user, account_name, account_num, '', url, session_id, '', 'All')
                ConfigurationOverviewServices.restart_request_trade_overview(user) # Reset is_trading và mua/bán tay

            # Kiểm tra tính hợp lệ của session
            if session_login_2 and validate_session(account_name, account_num, url, session_id, ''):
                result = update_vps_data(session_id, "Session hợp lệ!", 1)
                create_user_schedules(user)  # Bật scheduler của user (tạo PeriodicTask trong DB)
                user.scheduler_status = True
                user.save()
            else:
                return Response({"data": {"message": "Session chưa hợp lệ!", "status": 0}}, status=HTTP_400_BAD_REQUEST)

        return Response({"data": result}, status=HTTP_200_OK)


class AutomationLogoutStockExchangesView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def logout_smartone():
        print("Logout all account in smartOne vps has status login is LoginSuccess...")
        _ = AccountService.update_all_accounts_login_status()

    def post(self, requests):
        logout_status = AccountService.update_all_accounts_login_status()
        return Response({
            "data": {
                "message": "Update is successfully"
            }
        }, status=status.HTTP_200_OK)


class AutomationNotifyUserLoginView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def notify_login(user):
        accounts = AccountService.get_all_accounts()
        for account in accounts:
            if account.name == '361027':
                if account.login_status != AccountLoginStatusEnum.LoginSuccess.value:
                    notify_login = {
                        'user_account': account.name,
                        'platform_trading': 'Smart One'
                    }
                    send_message(user, MessageTypeEnum.OVERALL, SignalTelegramEnum.NOTIFY_LOGIN.value, **notify_login)

    @staticmethod
    def notify_running(user):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        vietnam_time = datetime.now(vietnam_tz)
        time = vietnam_time.strftime('%Y-%m-%d %H:%M:%S')
        notify_running = {
            'time': time
        }

        send_message(user, MessageTypeEnum.OVERALL, SignalTelegramEnum.NOTIFY_RUNNING.value, **notify_running)
