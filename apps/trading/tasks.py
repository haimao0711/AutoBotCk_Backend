from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from apps.account.detail.services import AccountService
from apps.trading.service.handlers import trading, cancel_all_orders, trading_request
from apps.configuration.details.overview.services import ConfigurationOverviewServices
from apps import api
import pytz
from datetime import datetime, time
from apps.trading.helper import is_within_range_time
from apps.telegram.sender import send_message_telegram, send_message
from apps.telegram.enum.enums import MessageTypeEnum
from common.errors.messages import ErrorMessages
from common.signal.enums import SignalTelegramEnum

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def user_trading_task(self, user_id):
    """
    Celery task thay thế cho TradingViews.user_trading
    """
    try:
        user = User.objects.get(id=user_id)
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(timezone).time()

        morning_start = time(9, 0)
        morning_end = time(14, 59)
        afternoon_start = time(13, 0)
        afternoon_end = time(14, 59)
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id
        
        logger.info(f'Đã chạy hàm user_trading của user {user.username} với tài khoản {account_num}')

        def notify_running(user):
            vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            vietnam_time = datetime.now(vietnam_tz)
            time_str = vietnam_time.strftime('%Y-%m-%d %H:%M:%S')
            notify_running_data = {
                'time': time_str,
                'username': user.username
            }
            send_message(user, MessageTypeEnum.OVERALL, SignalTelegramEnum.NOTIFY_RUNNING.value, **notify_running_data)
        is_market_time = is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end)
        
        if not is_market_time:
            logger.info(f"Ngoài giờ giao dịch cho user {user.username}. Bỏ qua lượt chạy.")
            return

        if session_id != 'stop_trading':
            notify_running(user)
            logger.info(f'📢📢📢Job trading của user {user.username} BẮT ĐẦU lượt chạy mới!')
            trading(user=user, vps_account=vps_account, symbol='All')
            
    except Exception as exc:
        logger.error(f'Error in user_trading_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        # Đóng connection của task hiện tại
        from django.db import connection
        connection.close()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def cancel_trading_task(self, user_id, job_type="morning"):
    """
    Celery task thay thế cho TradingViews.cancel_trading
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f'Job cancel all order is running for {job_type}')
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id
        url = api.TRADING_URL 
        
        cancel_all_orders(user, account_name, account_num, 'calendar_cancel', url, session_id, '', 'All')
        ConfigurationOverviewServices.restart_request_trade_overview(user) # Reset trạng thái toàn bộ
        
    except Exception as exc:
        logger.error(f'Error in cancel_trading_task: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def restart_request_trade_task(self, user_id):
    """
    Celery task thay thế cho TradingViews.restart_request_trade
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info('Job restart all request trade is running')
        ConfigurationOverviewServices.restart_request_trade_overview(user)
        
    except Exception as exc:
        logger.error(f'Error in restart_request_trade_task: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def trading_request_task(self, user_id, stock_id, symbol, request_buy, request_sell, volume_sell, is_use_chart_action):
    """
    Celery task thay thế cho TradingViews.request_trading
    """
    try:
        user = User.objects.get(id=user_id)
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(timezone).time()

        morning_start = time(9, 0)
        morning_end = time(14, 59)
        afternoon_start = time(13, 0)
        afternoon_end = time(14, 28)
        
        vps_account = AccountService.get_account_by_user(user)
        if not vps_account:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
            
        account_name = vps_account.name
        account_num = vps_account.account_num
        session_id = vps_account.vps_session_id
        type_request_trading = 'Mua tay' if request_buy else 'Bán tay'
        if is_within_range_time(now, morning_start, morning_end) or is_within_range_time(now, afternoon_start, afternoon_end):
            url = api.TRADING_URL
            if session_id != 'stop_trading':
                logger.info(f'Yêu cầu {type_request_trading} mã {symbol} user {user.username} BẮT ĐẦU thực hiện!')
                
                # Chạy trading_request trong Celery task
                result = trading_request(user, vps_account, stock_id, symbol, request_buy, request_sell, volume_sell, is_use_chart_action)
                return result
                
        return False
        
    except Exception as exc:
        logger.error(f'Error in trading_request_task: {exc}')
        raise self.retry(exc=exc)
