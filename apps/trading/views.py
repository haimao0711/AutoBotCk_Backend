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
from apps.trading.helper import is_within_range_time
from apps.trading.service.utils import is_within_time_range
from datetime import datetime, time
from common.api.smartone.handler import validate_session
from apps.telegram.sender import send_message_telegram
from common.api.smartone.handler import handle_stock_balance_service
from common.errors.messages import ErrorMessages
from apps import api
import threading

# Lưu các thread giao dịch đang hoạt động
active_trading_threads = {}

class TradingViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requests):
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        TradingViews.user_trading()
        return Response({
            "data": []
        }, status=status.HTTP_200_OK)    

    @staticmethod
    def user_trading(user):
        try:   
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(timezone).time()

            morning_start = time(9, 15)
            morning_end = time(23, 28)
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
        try:   
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(timezone).time()

            morning_start = time(9, 15)
            morning_end = time(11, 30)
            afternoon_start = time(13, 0)
            afternoon_end = time(14, 28)
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id

           
            if is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end):
            # if user.username == 'tranhaimao':
                url = api.TRADING_URL
                res_validate_session = validate_session(account_name, account_num, url, session_id, '')
                if not res_validate_session:
                    message = 'Session chưa hợp lệ. Bot không thực hiện trading được!'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message)  
                    return False
                
                if session_id != 'stop_trading' and res_validate_session:
                    print('Request trading BẮT ĐẦU thực hiện !')

                    # Kiểm tra xem có thread nào đang chạy cho cổ phiếu này không
                    key = f"{user.id}_{stock_id}"
                    if key in active_trading_threads:
                        print(f"Đang có giao dịch cho cổ phiếu {stock_id} của user {user.id}!")
                        return False  # Đang có tiến trình khác, không xử lý giao dịch mới

                    # Tạo stop_event để dừng giao dịch khi cần
                    stop_event = threading.Event()
                    thread = threading.Thread(
                        target=trading_request,
                        args=(user, vps_account, stock_id, symbol, request_buy, request_sell, volume_sell),
                        daemon=True
                    )
                    thread.start()

                    # Lưu trữ thread và stop_event vào active_trading_threads
                    active_trading_threads[key] = {'thread': thread, 'stop_event': stop_event}

                    return True  # Trả về True nếu giao dịch được bắt đầu

                return False
            else:
                message = 'Chưa đến thời gian giao dịch của sàn. Vui lòng thử lại sau'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message)  
        except Exception as e:
            print(f"Unexpected error: {e}")
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
            print('Job cancel all order is running')
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            account_name = vps_account.name
            account_num = vps_account.account_num
            session_id = vps_account.vps_session_id
            url = api.TRADING_URL 
            cancel_buy_order(user, account_name, account_num, symbol, url, session_id, 'Lệnh mua tay còn đặt', "B")
            cancel_sell_order(user, account_name, account_num, symbol, url, session_id, 'Lệnh bán tay còn đặt', "S")
               
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
            # print('check status_scheduler: ', status_scheduler)
            url = api.TRADING_URL

            is_valid_session, financial_data = validate_session(account_name, account_num, url, session_id, '')

            # print('check is_valid_session: ', is_valid_session)
            # print('check financial_data: ', financial_data)
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
                    "limit_number_stocks": limit_number_stocks ,
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
                    "limit_number_stocks":limit_number_stocks,
                })
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")
            return Response({"error": str(e)}, status=500)
    