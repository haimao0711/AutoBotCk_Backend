from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime
import pytz

# from apps.trading.service.signals import trading
from common.signal.enums import SignalTelegramEnum
from apps.telegram.enum.enums import MessageTypeEnum
from apps.telegram.sender import send_message
from apps.authencation.user.models import User
from apps.account.detail.models import Account
from apps.account.detail.services import AccountService
from apps.account.detail.enums import AccountLoginStatusEnum
from apps.configuration.details.overview.services import ConfigurationOverviewServices
from apps.trading.service.handlers import trading, trading_request, cancel_all_orders, cancel_buy_order, cancel_sell_order
from apps.trading.tasks import user_trading_task, trading_request_task
from apps.trading.scheduler.celery_scheduler import create_user_schedules, remove_user_schedules, get_user_schedule_status
from apps.trading.helper import is_within_range_time
from apps.trading.service.utils import is_within_time_range
from datetime import datetime, time
from common.api.smartone.handler import validate_session
from apps.telegram.sender import send_message_telegram
from common.api.smartone.handler import handle_stock_balance_service
from common.errors.messages import ErrorMessages
from apps import api
import threading

# Test endpoints không cần authentication
class TestAPIView(APIView):
    permission_classes = []  # Không cần authentication
    
    def get(self, request):
        return Response({
            "message": "Test API hoạt động!",
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }, status=status.HTTP_200_OK)

class TestSchedulerStatusView(APIView):
    permission_classes = []  # Không cần authentication
    
    def get(self, request):
        try:
            from apps.trading.scheduler.celery_scheduler import get_user_schedule_status
            
            # Test với user đầu tiên
            from apps.authencation.user.models import User
            user = User.objects.first()
            
            if user:
                status_info = get_user_schedule_status(user)
                return Response({
                    "message": "Scheduler status test",
                    "user": user.username,
                    "status": status_info,
                    "timestamp": datetime.now().isoformat()
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Không có user nào",
                    "status": "no_users"
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({
                "message": f"Lỗi: {str(e)}",
                "status": "error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Lưu các thread giao dịch đang hoạt động
active_trading_threads = {}

class TradingViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requests):
        # Dispatch Celery task thay vì chạy trực tiếp
        user_trading_task.delay(requests.user.id)
        return Response({
            "message": "Trading task đã được dispatch",
            "data": []
        }, status=status.HTTP_200_OK)    

    @staticmethod
    def user_trading(user):
        try:   
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(timezone).time()

            morning_start = time(9, 15)
            morning_end = time(11, 28)
            afternoon_start = time(13, 0)
            afternoon_end = time(14, 28)
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            print(f'đã chạy hàm user_trading của user {account_name} với tài khoản {account_num}')

            def notify_running(user):
                vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                vietnam_time = datetime.now(vietnam_tz)
                time = vietnam_time.strftime('%Y-%m-%d %H:%M:%S')
                notify_running = {
                    'time': time,
                    'username': user.username
                }

                send_message(user, MessageTypeEnum.OVERALL, SignalTelegramEnum.NOTIFY_RUNNING.value, **notify_running)

            if is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end):
            # if user.username == 'tranhaimao':
                url = api.TRADING_URL
                is_validate_session, res_validate_session = validate_session(account_name, account_num, url, session_id, '')
                if not is_validate_session:                  
                    message = 'Mã phiên giao dịch chưa hợp lệ. Vui lòng nhập lại OTP!'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message)  
                if session_id != 'stop_trading' and is_validate_session:
                    notify_running(user)
                    print('Bot BAT DAU thực hiện trading!')
                    trading(user=user, vps_account=vps_account, symbol='All')
                
        except Exception as e:
            print(f"Unexpected error: {e}")
    

    @staticmethod
    def request_trading(user, stock_id: str, symbol: str, request_buy: bool, request_sell: bool, volume_sell: str):
        # Dispatch Celery task thay vì chạy trực tiếp
        result = trading_request_task.delay(
            user.id, stock_id, symbol, request_buy, request_sell, volume_sell
        )
        try:
            return result.get(timeout=30)  # Wait for result with timeout
        except Exception as e:
            print(f"Error in trading_request_task: {e}")
            return False

    @staticmethod
    def cancel_trading(user):
        try:   
            print('Job cancel all order is running')
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            url = api.TRADING_URL 
            cancel_all_orders(user, account_name, account_num, '', url, session_id, '', 'All')
               
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def cancel_request_oder(user, symbol):
        try:   
            print('Job cancel_request_oder is running')
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            url = api.TRADING_URL 
            cancel_buy_order(user, account_name, account_num, symbol, url, session_id, 'Yêu cầu ngừng mua tay', "B")
            cancel_sell_order(user, account_name, account_num, symbol, url, session_id, 'Yêu cầu ngừng bán tay', "S")
               
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def restart_request_trade(user):
        try:   
            print('Job restart all request trade is running')
            ConfigurationOverviewServices.restart_request_trade_overview(user)
               
        except Exception as e:
            print(f"Unexpected error: {e}")


class TradingViewsIsTrading(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user          
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            limit_number_stocks = vps_account.limit_number_stocks
            status_scheduler = user.scheduler_status
            url = api.TRADING_URL

            is_valid_session, financial_data = validate_session(account_name, account_num, url, session_id, '')
            is_trading = is_valid_session and status_scheduler
            
            if financial_data:
                return Response({
                    "is_trading": is_trading,
                    "account_name": account_name,
                    "account_num": account_num,
                    "total_equity": financial_data.get("total_equity", 0),
                    "cash_balance": financial_data.get("cash_balance", 0),
                    "total_market_value": financial_data.get("total_market_value", 0),
                    "cash_available": financial_data.get("cash_available", 0),
                    "limit_number_stocks": limit_number_stocks,
                })
            else:
                return Response({
                    "is_trading": is_trading,
                    "account_name": account_name,
                    "account_num": account_num,
                    "total_equity": 0,
                    "cash_balance": 0,
                    "total_market_value": 0,
                    "cash_available": 0,
                    "limit_number_stocks": limit_number_stocks,
                })
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")
            return Response({"error": str(e)}, status=500)


class StartSchedulerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        success = create_user_schedules(user)
        if success:
            user.scheduler_status = True
            user.save()
            return Response({"message": f"Scheduler started for user {user.username}!"}, status=200)
        else:
            return Response({"error": "Failed to start scheduler"}, status=500)


class StopSchedulerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        success = remove_user_schedules(user)
        if success:
            user.scheduler_status = False
            user.save()
            return Response({"message": f"Scheduler stopped for user {user.username}!"}, status=200)
        else:
            return Response({"error": "Failed to stop scheduler"}, status=500)


class SchedulerStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        status = get_user_schedule_status(user)
        return Response(status, status=200)
    