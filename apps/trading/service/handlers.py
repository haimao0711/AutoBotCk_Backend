from django.utils import timezone
from django.db import connection, close_old_connections
from datetime import datetime
import pytz

from apps.authencation.user.models import User
from apps.account.models import Account

from apps.stock.models import Stock
from apps.stock.enums import DownloadStatusEnum
from apps.stock.services import DownloadService, StockService

from apps.configuration.details.models import Configuration
from apps.configuration.details.services import ConfigurationServices
from apps.configuration.candle.enums import CandleEnum
from apps.stock.models import StockM1, StockD1, StockM5, StockM15, StockH1

from apps.trading.enum.enums import ChartType
from apps.trading.service.constants import VALID_TIME_REQUEST_BUY, VALID_TIME_REQUEST_SELL
from apps.trading.service.download import download_data, download_sales_volume
from apps.trading.service.helper import (render_message, round_to_nearest_hundred, should_sell_take_profit, should_take_profit_bolinger, is_valid_time_to_buy, is_valid_time_to_sell,
                                         send_telegram_message, send_telegram_message_batch, should_buy, should_buy_following, should_buy_trading, should_sell, should_sell_trading)
from apps.trading.service.utils import round_up_to_unit, revert_status_request_trade
from apps.telegram.sender import send_message, send_message_telegram

# from apps.balance.services import BalanceService

from common.signal.enums import SignalTelegramEnum
from common.success.types import SuccessType
from apps.telegram.enum.enums import MessageTypeEnum
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed
from common.api.smartone.handler import (handle_buy_service, handle_sell_service, handle_update_order_service, handle_cancel_order_service,
                                         handle_orders_not_matched, handle_orders_matched, handle_stock_balance_service, handle_transaction_service, handle_cash_balance_service)
from apps.configuration.details.services import ConfigurationServices
from apps.stock.services import DownloadService
from apps.account.detail.services import AccountService
from apps import api
import pandas as pd
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

import threading
import logging
logger = logging.getLogger(__name__)



def cancel_all_orders(user: User, user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str):
    logger.info(f'Bắt đầu chạy hàm cancel all order ')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, side)
       
    if res_not_matcheds:
        logger.info(f'Da co danh sach chua khop to cancel all order: {res_not_matcheds}')

        for order in res_not_matcheds: 
            # Sử dụng helper execute_action_with_retry
            res_cancel = execute_action_with_retry(
                handle_cancel_order_service,
                user_name, request_url, session, '', order['orderNo'], ref_id,
                action_name=f"Cancel All Orders - {order['symbol']}"
            )
            
            if res_cancel:
                logger.info(f"Da huy lenh {order['side']} mã {order['symbol']}: {res_cancel}")
            else:
                logger.info(f'Chua huy duoc lenh sell {symbol}')
        message_cancel = '📢📢📢** Khởi động lại Bot, đã hủy tất cả các lệnh đang đặt hiện tại** 📢📢📢'
        if symbol == 'calendar_cancel':
            message_cancel = '📢📢📢** Hủy tất cả các lệnh đang đặt hiện tại theo lịch** 📢📢📢'
        elif symbol == 'cancel_all_buy_orders':
            message_cancel = '** Chặn mua, đã hủy tất cả các lệnh mua đang đặt hiện tại**'
        else:
            message_cancel = '** Đã hủy tất cả các lệnh đang đặt hiện tại**'        
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_cancel)
        send_message_telegram(user, MessageTypeEnum.ACT, message_cancel)        
 
    else:
        logger.info(f'Chua lay duoc danh sach chua khop to cancel all orders')
def cancel_all_buy_orders(user: User, user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str):
    logger.info(f'Bắt đầu chạy hàm cancel all buy orders ')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, side)
       
    if res_not_matcheds:
        logger.info(f'Da co danh sach chua khop to cancel all buy orders: {res_not_matcheds}')

        for order in res_not_matcheds: 
            # Sử dụng helper execute_action_with_retry
            res_cancel = execute_action_with_retry(
                handle_cancel_order_service,
                user_name, request_url, session, '', order['orderNo'], ref_id,
                action_name=f"Cancel All Buy Orders - {order['symbol']}"
            )
            
            if res_cancel:
                logger.info(f"Da huy lenh {order['side']} mã {order['symbol']}: {res_cancel}")
            else:
                logger.info(f"Chua huy duoc lenh {order['side']}  {symbol}")
        message_cancel = '** Chặn mua, đã hủy tất cả các lệnh mua đang đặt hiện tại**'
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_cancel)
        send_message_telegram(user, MessageTypeEnum.ACT, message_cancel)
    else:
        logger.info(f'Chua lay duoc danh sach chua khop to cancel all buy orders')
def cancel_all_sell_orders(user: User, user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str):
    logger.info(f'Bắt đầu chạy hàm cancel all sell orders ')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, side)
       
    if res_not_matcheds:
        logger.info(f'Da co danh sach chua khop to cancel all sell orders: {res_not_matcheds}')

        for order in res_not_matcheds: 
            # Sử dụng helper execute_action_with_retry
            res_cancel = execute_action_with_retry(
                handle_cancel_order_service,
                user_name, request_url, session, '', order['orderNo'], ref_id,
                action_name=f"Cancel All Sell Orders - {order['symbol']}"
            )
            
            if res_cancel:
                logger.info(f"Da huy lenh {order['side']} mã {order['symbol']}: {res_cancel}")
            else:
                logger.info(f"Chua huy duoc lenh {order['side']}  {symbol}")
        message_cancel = '** Chặn bán, đã hủy tất cả các lệnh bán đang đặt hiện tại**'
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_cancel)
        send_message_telegram(user, MessageTypeEnum.ACT, message_cancel)
    else:
        logger.info(f'Chua lay duoc danh sach chua khop to cancel all sell orders')

def get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, side, max_retry=3, retry_delay=1):
    """
    Helper function to get unmatched orders with retry mechanism.
    """
    retry_count = 0
    res_not_matcheds = None
    
    while not res_not_matcheds and retry_count < max_retry:
        try:
            res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', side)
        except Exception as e:
            logger.error(f"Lỗi khi gọi handle_orders_not_matched (Lần {retry_count + 1}/{max_retry}): {e}")
            res_not_matcheds = None

        if not res_not_matcheds:
            retry_count += 1
            if retry_count < max_retry:
                logger.info(f"Lần thử {retry_count}/{max_retry}: Chưa có danh sách chưa khớp cho symbol {symbol}. Thử lại sau {retry_delay} giây...")
                time.sleep(retry_delay)
    
    return res_not_matcheds

def execute_action_with_retry(action_func, *args, max_retry=3, retry_delay=2, action_name="Action"):
    """
    Helper function to execute an action (update/cancel) with retry mechanism.
    """
    retry_count = 0
    result = None
    
    while not result and retry_count < max_retry:
        try:
            result = action_func(*args)
        except Exception as e:
            logger.error(f"Lỗi khi thực hiện {action_name} (Lần {retry_count + 1}/{max_retry}): {e}")
            result = None
            
        if not result:
            retry_count += 1
            if retry_count < max_retry:
                logger.info(f"Thực hiện {action_name} thất bại. Thử lại lần {retry_count}/{max_retry} sau {retry_delay} giây...")
                time.sleep(retry_delay)
                
    return result



def update_buy_order(user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str, step_price: float, limited_price: float, times_update: int):
    logger.info(f'Bắt đầu chạy hàm update lệnh mua {symbol} ' )    
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time_update = datetime.now(tz).strftime("%H:%M:%S ngày %d-%m-%Y")
    start_time = time.time()  # Lấy thời gian bắt đầu
    logger.info(f'Nhắc lại giới hạn update lệnh mua {symbol}: {limited_price}' )
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, 'B')

    message_buy_update = []

    if res_not_matcheds:
        logger.info(f"Đã có danh sách chưa khớp để update buy stock {symbol}: {res_not_matcheds}")
        buy_update_overrall_attrs = {        
            'user_account': account,
            'stock': symbol,
            'number_order': len(res_not_matcheds),
            'start_time_order': start_time_update,
            'times_update': times_update
        } 
        message_buy_update.append({
            'status_signal': SignalTelegramEnum.BUY_UPDATE_OVERRAL,
            **buy_update_overrall_attrs
        })               
        for order in res_not_matcheds:   
            ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"   
            old_price = float(order['showPrice'])
            update_price = round(old_price + step_price, 2)            
            update_volume = int(order['volume'])
            order_num = order['orderNo']
            try:
            # Nếu update_price chưa vượt limited_price thì handle update order
                if update_price < limited_price:
                    # Sử dụng helper execute_action_with_retry
                    res_update_order = execute_action_with_retry(
                        handle_update_order_service, 
                        user_name, account, request_url, symbol, session, '', order_num, old_price, update_price, update_volume, ref_id, 'B',
                        action_name="Update Buy Order"
                    )
                    
                    if res_update_order:
                        buy_update_details_attrs = {
                            'stock': order['symbol'],
                            'old_price': old_price,
                            'update_price': update_price,
                            'volume': order['volume'],
                            'status': order['status']
                        }
                        
                        message_buy_update.append({
                                'status_signal': SignalTelegramEnum.BUY_UPDATE_DETAIL,
                                **buy_update_details_attrs
                        })
                    else:
                        logger.info(f'Chua update duoc lenh mua one order {symbol}')
                
            # Nếu update_price vượt quá limited_price thì handle cancel order
                else:
                    logger.info(f'Huy lenh vi gia update: {update_price} da toi limited: {limited_price}')
                    # Sử dụng helper execute_action_with_retry
                    res_cancel_order = execute_action_with_retry(
                        handle_cancel_order_service,
                        user_name, request_url, session, '', order_num, ref_id,
                        action_name="Cancel Buy Order (Limit Reached)"
                    )
                    
                    if res_cancel_order:
                        logger.info(f'Da huy lenh mua {symbol}: {res_cancel_order}')
                        buy_cancel_details_attrs = {
                            'stock': order['symbol'],
                            'price': order['showPrice'],
                            'volume': order['volume'],
                            'status': 'Đã hủy'
                        }
                        message_buy_update.append({
                            'status_signal': SignalTelegramEnum.BUY_CANCEL_DETAIL,
                            **buy_cancel_details_attrs
                        })
                    else:
                        logger.info(f'Chua huy duoc lenh mua one order {symbol}')
            except Exception as e:
                logger.info(f"[ERROR] Lỗi khi xử lý order {order_num}: {e}")
    else:
        logger.info(f"Không có danh sách chưa khớp để update buy stock {symbol}. Ngưng update lệnh")

    return message_buy_update


def cancel_buy_order(user: User,user_name: str, account: str, symbol: str, request_url: str, session: str, reason: str, side: str):
    logger.info(f'Bắt đầu chạy hàm cancel buy oders {symbol} ' )
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    # start_time_cancel = datetime.now(timezone)
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time_cancel = datetime.now(tz).strftime("%H:%M:%S ngày %d-%m-%Y")
    message_buy_cancel = []
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, 'B')
        
    if res_not_matcheds:
        logger.info(f'Da co danh sach chua khop to cancel buy stock {symbol}: {res_not_matcheds}')
        buy_cancel_overrall_attrs = {        
            'user_account': account,
            'stock': symbol,
            'reason': reason,
            'number_order': len(res_not_matcheds),
            'start_time_order': start_time_cancel
        } 
        message_buy_cancel.append({
            'status_signal': SignalTelegramEnum.BUY_CANCEL_OVERRAL,
            **buy_cancel_overrall_attrs
        })            

        for order in res_not_matcheds:  
            # Sử dụng helper execute_action_with_retry
            res_cancel = execute_action_with_retry(
                handle_cancel_order_service,
                user_name, request_url, session, '', order['orderNo'], ref_id,
                action_name="Cancel Buy Order"
            )
            
            if res_cancel:
                logger.info(f'Da huy lenh mua {symbol}: {res_cancel}')
                buy_cancel_details_attrs = {
                    'stock': order['symbol'],
                    'price': order['showPrice'],
                    'volume': order['volume'],
                    'status': 'Đã hủy'
                }
                message_buy_cancel.append({
                    'status_signal': SignalTelegramEnum.BUY_CANCEL_DETAIL,
                    **buy_cancel_details_attrs
                })
            else:
                logger.info(f'Chua huy duoc lenh mua {symbol}')

        if message_buy_cancel:
            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_buy_cancel)
            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_buy_cancel)
    else:
        logger.info(f'Chua lay duoc danh sach chua khop to cancel buy {symbol}')  
    logger.info(f'Kết thúc chạy hàm cancel lệnh mua {symbol} ' )

def update_sell_order(user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str, step_price: float, limited_price: float, times_update: int):
    logger.info(f'Bắt đầu chạy hàm update lệnh bán {symbol} ' )      
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    time_now  = datetime.now(tz)
    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")    
    
    message_sell_update = []
    logger.info(f'Nhắc lại giới hạn update lệnh bán {symbol}: {limited_price}')
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, 'S')
         
    if res_not_matcheds:
        logger.info(f'da co danh sach chưa khơp to update stock {symbol}: {res_not_matcheds}') 
        sell_update_overrall_attrs = {        
            'user_account': account,
            'stock': symbol,
            'number_order': len(res_not_matcheds),
            'start_time_order': start_time_order,
            'times_update': times_update
            } 
        message_sell_update.append({
            'status_signal': SignalTelegramEnum.SELL_UPDATE_OVERRAL,
            **sell_update_overrall_attrs
        })
            
        for order in res_not_matcheds:      
            ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
            old_price = float(order['showPrice'])
            update_price = round(old_price - step_price, 2)      
            update_volume = int(order['volume'])
            order_num = order['orderNo']
            logger.info(f'check order_num sell: {order_num}')
        # Nếu update_price chưa bé hơn limited_price thì handle update order
            if update_price > limited_price:
                # Sử dụng helper execute_action_with_retry
                res_update_order = execute_action_with_retry(
                    handle_update_order_service,
                    user_name, account, request_url, symbol, session, '', order_num, old_price, update_price, update_volume, ref_id, 'S',
                    action_name="Update Sell Order"
                )
                
                if res_update_order:
                    sell_update_details_attrs = {
                        'stock': order['symbol'],
                        'old_price': old_price,
                        'update_price': update_price,
                        'volume': order['volume'],
                        'status': order['status']
                        }
                    message_sell_update.append({
                        'status_signal': SignalTelegramEnum.SELL_UPDATE_DETAIL,
                        **sell_update_details_attrs
                        })            
        # Nếu update_price nhỏ hơn limited_price thì handle cancel order
            else:
                logger.info(f'Huy lenh vi gia update: {update_price} da toi limited: {limited_price}')
                # Sử dụng helper execute_action_with_retry
                res_cancel_order = execute_action_with_retry(
                    handle_cancel_order_service,
                    user_name, request_url, session, '', order_num, ref_id,
                    action_name="Cancel Sell Order (Limit Reached)"
                )
                
                if res_cancel_order:
                    sell_cancel_details_attrs = {
                        'stock': res_cancel_order['symbol'],
                        'price': res_cancel_order['showPrice'],
                        'volume': res_cancel_order['volume'],
                        'status': 'Đã hủy'
                        }
                    message_sell_update.append({
                        'status_signal': SignalTelegramEnum.SELL_CANCEL_DETAIL,
                        **sell_cancel_details_attrs
                    })
                else:
                    logger.info(f'Chua huy duoc lenh mua one order {symbol}') 
    else: 
        logger.info(f'chưa lấy được res danh sach chưa khơp to update sell {symbol} ' )

    return message_sell_update  

def cancel_sell_order(user: User, user_name: str, account: str, symbol: str, request_url: str, session: str, reason: str, side: str):
    logger.info(f'Bắt đầu chạy hàm cancel lệnh sell {symbol}')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    time_now  = datetime.now(tz)
    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y") 
    message_cancel = []
    
    # Sử dụng helper function với retry
    res_not_matcheds = get_orders_not_matched_with_retry(user_name, account, symbol, request_url, session, 'S')
       
    if res_not_matcheds:
        logger.info(f'Da co danh sach chua khop to cancel sell stock {symbol}: {res_not_matcheds}')
        sell_cancel_overrall_attrs = {        
            'user_account': account,
            'stock': symbol,
            'reason': reason,
            'number_order': len(res_not_matcheds),
            'start_time_order': start_time_order
        } 
        message_cancel.append({
            'status_signal': SignalTelegramEnum.SELL_CANCEL_OVERRAL,
            **sell_cancel_overrall_attrs
        })            
        
        for order in res_not_matcheds: 
            # Sử dụng helper execute_action_with_retry
            res_cancel = execute_action_with_retry(
                handle_cancel_order_service,
                user_name, request_url, session, '', order['orderNo'], ref_id,
                action_name="Cancel Sell Order"
            )
            
            if res_cancel:
                logger.info(f'Da huy lenh ban {symbol}: {res_cancel}')
                sell_cancel_details_attrs = {
                    'stock': order['symbol'],
                    'price': order['showPrice'],
                    'volume': order['volume'],
                    'status': 'Đã hủy'
                }
                message_cancel.append({
                    'status_signal': SignalTelegramEnum.SELL_CANCEL_DETAIL,
                    **sell_cancel_details_attrs
                })
            else:
                logger.info(f'Chua huy duoc lenh sell {symbol}')
                pass
        # Send telegram   
        if message_cancel:
            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_cancel)
            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_cancel)
    else:
        logger.info(f'Chua lay duoc danh sach chua khop to cancel sell {symbol}')  

def process_buy_request(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, stock_id: str, limit_number_stocks: int, request_buy: bool, request_sell: bool, is_use_chart_action: bool):
    # Các giá trị mặc định
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    user_name = vps_account.name
    account = vps_account.account_num
    session = vps_account.vps_session_id
    request_url = api.TRADING_URL
    ref_id = f"{user_name}.I.test.{int(time.time() * 1000)}"    

    # Lấy dữ liệu đã chuẩn bị  
    trading_candle = prepared["trading_candle"]
    trading_candle_second = prepared["trading_candle_second"]
    following_candle = prepared["following_candle"]
    following_candle_second = prepared["following_candle_second"]
    trading_chart_type = prepared["trading_chart_type"]
    trading_chart_type_second = prepared["trading_chart_type_second"]
    following_chart_type = prepared["following_chart_type"]
    following_chart_type_second = prepared["following_chart_type_second"]
    trading_config = prepared["trading_config"]
    following_config = prepared["following_config"]       
    overview_config = prepared["overview_config"]
    stock = prepared["stock"]
    symbol = stock.name
    
    logger.info(f'check is_use_chart_action {symbol}: {is_use_chart_action}')        
    asp_net_session = ''
    max_stock_existing = limit_number_stocks
    slippage_buy = trading_config.stock_config_slippage_buy
    add_price_buy = trading_config.stock_config_add_price_buy
    level = overview_config.level
    is_time_valid_to_buy = is_valid_time_to_buy(following_config)
    #HANDLE BUY
    if is_time_valid_to_buy:
        try:
            # Xác định thời gian bắt đầu và thời gian kết thúc (sau 1 tiếng)
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=2)
            status_buy = SignalTelegramEnum.BUY_REQUEST_FAILED
            last_buy_check_time = None  # Dùng để giới hạn việc kiểm tra mua mỗi 60 giây
            message_stop_buy = 'Hết thời gian của lệnh mua tay'
            price_to_start = None  # Khởi tạo giá trị mặc định để tránh lỗi khi sử dụng sau vòng lặp
            logger.info(f"DEBUG: Entering process_buy_request try block for {symbol}")
            update_status, update_data = ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
            logger.info(f"DEBUG: update_status={update_status}, expected={SuccessType.UPDATED_SUCCESS}")
            if update_status != SuccessType.UPDATED_SUCCESS:
                logger.error(f'Failed to update is_trading for {symbol}: {update_data}')
                message_fail = f'⚠️ Đưa {symbol} vào danh sách đang hoạt động thất bại. Hủy yêu cầu mua tay!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_fail)
                send_message_telegram(user, MessageTypeEnum.ACT, message_fail)
                return
            if not is_use_chart_action:
                logger.info(f'Xu ly lenh mua ngay {symbol}')
                # Tải dữ liệu       
                vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                    stock=stock,
                    vnindex_stock=vnindex_stock,
                    trading_chart_type=trading_chart_type,
                    following_chart_type=following_chart_type
                )
                if stock_data_trading is None:
                    logger.info('Download data không thành công (chart action), bỏ qua!')
                    message_download = f'Không tải được dữ liệu mã {symbol} từ Chart Action, hủy yêu cầu mua tay. Vui lòng thử lại sau ít phút'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                    send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                    return

                price_to_start = (stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close']) / 2
                status_buy = SignalTelegramEnum.BUY_REQUEST_SUCCESS
                messages_to_buy = 'Mua ngay'
                time_now = datetime.now(timezone)
                start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")

                buy_attrs = {
                    "user_account": account,
                    "platform_trading": "Smart One",
                    "stock": stock.name,
                    "level": level,
                    "price": price_to_start,
                    "message": messages_to_buy,
                    "start_time_order": start_time_order,
                }
                send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)

            while is_use_chart_action and datetime.now() < end_time:
                close_old_connections()
                logger.info(f'Xu ly lenh mua tay theo chart {symbol} ')
                # Kiểm tra is_buy_hand mỗi 3 giây        
                try:
                    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
                    overview_config = configuration.get("overview_config", {})
                    is_buy_hand = overview_config.is_buy_hand
                    logger.info(f'check is_buy_hand overview_config {symbol}: {is_buy_hand}')
                except Exception as e:
                    logger.error(f'Lỗi khi lấy lại cấu hình mua tay cho {symbol}: {e}')
                    connection.close()  # Close connection before sleep
                    time.sleep(1)
                    continue

                if not is_buy_hand:
                    logger.info(f'Dừng mua tay cổ phiếu {symbol}: {is_buy_hand}')
                    message_stop_buy = 'Đã yêu cầu ngừng mua tay'
                    break  # Thoát khỏi vòng while và tiếp tục đoạn code phía sau

                # Kiểm tra điều kiện mua chỉ mỗi 60 giây một lần
                now = datetime.now()
                if last_buy_check_time is None or (now - last_buy_check_time).total_seconds() >= 60:
                    last_buy_check_time = now

                    # === XỬ LÝ MUA ===     
                    # Tải dữ liệu lần 1       
                    vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                        stock=stock,
                        vnindex_stock=vnindex_stock,
                        trading_chart_type=trading_chart_type,
                        following_chart_type=following_chart_type
                    )
                    # Tải dữ liệu lần 2
                    vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_second, 
                        following_chart_type=following_chart_type_second
                    )
                    if stock_data_trading is None:
                        logger.info('Download data không thành công, bỏ qua!')
                        message_download = f'Không tải được dữ liệu mã {symbol}, hủy yêu cầu mua tay. Vui lòng thử lại sau ít phút'
                        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                        send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                        return

                    price_to_start = (
                        stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close']) / 2

                    # 🔄 Lấy lại prepared mới mỗi lần lặp để cập nhật cấu hình mới nhất
                    try:
                        configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                            user=user, 
                            stock_symbol=symbol
                        )
                        if configuration:
                            refreshed_trading_config = configuration.get("trading_config")
                            refreshed_following_config = configuration.get("following_config")
                            refreshed_overview_config = configuration.get("overview_config")
                            refreshed_stock = configuration.get("stock")
                    
                            # Cập nhật các biến config nếu lấy được
                            if refreshed_trading_config:
                                trading_config = refreshed_trading_config
                                trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
                                trading_candle_second = getattr(getattr(trading_config, "candle_second", None), "candle", "M5")
                                trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
                                trading_chart_type_second = getattr(CandleEnum, trading_candle_second, CandleEnum.M5)
                            if refreshed_following_config:
                                following_config = refreshed_following_config
                                following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
                                following_candle_second = getattr(getattr(following_config, "candle_second", None), "candle", "D1")
                                following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
                                following_chart_type_second = getattr(CandleEnum, following_candle_second, CandleEnum.D1)
                            if refreshed_overview_config:
                                overview_config = refreshed_overview_config
                            if refreshed_stock:
                                stock = refreshed_stock
                    except Exception as e:
                        logger.info(f'Lỗi khi lấy lại cấu hình cho {symbol}: {e}')
                        connection.close()
                        # Tiếp tục dùng config cũ nếu lỗi

                    is_buy, buy_reason = should_buy_trading(
                        trading_config=trading_config,
                        data_trading_df=stock_data_trading,
                        config_type='stock_config',
                        data_trading_df_second=stock_data_trading_second
                    )

                    if is_buy:
                        status_buy = SignalTelegramEnum.BUY_REQUEST_SUCCESS

                    messages_to_buy = render_message(
                        buy_reason, trading_chart_value=trading_candle, trading_chart_value_second=trading_candle_second, following_chart_type=following_candle, following_chart_type_second=following_candle_second
                    )
                    time_now = datetime.now(timezone)
                    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")

                    buy_attrs = {
                        "user_account": account,
                        "platform_trading": "Smart One",
                        "stock": stock.name,
                        "level": level,
                        "price": price_to_start,
                        "message": messages_to_buy,
                        "start_time_order": start_time_order,
                    }

                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)

                    if status_buy == SignalTelegramEnum.BUY_REQUEST_SUCCESS:
                        logger.info('Dừng vòng lặp do điều kiện mua thoả mãn.')
                        break

                for _ in range(3):
                    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
                    overview_config = configuration.get("overview_config", {})
                    if not overview_config.is_buy_hand:
                        logger.info(f"Phát hiện tắt mua tay trong lúc chờ đợi, thoát vòng lặp.")
                        break
                    time.sleep(1)

            if status_buy == SignalTelegramEnum.BUY_REQUEST_FAILED:
                logger.info('Dừng vòng lặp do vượt thời gian hoặc Yêu cầu ngừng mua tay .')        
                # revert_status_request_trade removed here, handled in finally
                time_now = datetime.now(timezone)
                start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                # Nếu price_to_start chưa được khởi tạo, download data một lần nữa để lấy giá
                if price_to_start is None:
                    try:                
                        _, _, stock_data_trading_temp, _ = download_data(
                            stock=stock,
                            vnindex_stock=vnindex_stock,
                            trading_chart_type=trading_chart_type,
                            following_chart_type=following_chart_type
                        )
                        if stock_data_trading_temp is not None and len(stock_data_trading_temp) > 0:
                            price_to_start = (stock_data_trading_temp.iloc[-1]['open'] + stock_data_trading_temp.iloc[-1]['close']) / 2
                        else:
                            price_to_start = 0  # Giá trị mặc định nếu không lấy được
                    except Exception as e:
                        logger.error(f"Lỗi khi download data để lấy price_to_start: {e}")
                        price_to_start = 0  # Giá trị mặc định nếu có lỗi
                buy_attrs = {
                    "user_account": account,
                    "platform_trading": "Smart One",
                    "stock": stock.name,
                    "level": level,
                    "price": price_to_start if price_to_start is not None else 0,
                    "message": message_stop_buy,
                    "start_time_order": start_time_order,
                }
                try:
                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
                except Exception as e:
                    logger.info(f"❌ Lỗi khi gửi tin nhắn: {e}") 

            is_send_order_buy = False   
            if status_buy == SignalTelegramEnum.BUY_REQUEST_SUCCESS:
                logger.info(f'bắt đầu hàm đặt lệnh mua tay {symbol}')
                timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                last_row = stock_data_trading.iloc[-1]
                open_last_row = last_row['open'] 
                close_last_row = last_row['close']
                low_last_row = last_row['low']            
                high_last_row = last_row['high']
                step_price = trading_config.stock_config_slippage_volume_buy_per_pid
                time_to_buy = trading_config.stock_config_time_to_buy
                time_to_buy = time_to_buy if time_to_buy > 30 else 30
                sleeping_time_buy = trading_config.stock_config_time_update_pid_buy
                sleeping_time_buy = sleeping_time_buy if sleeping_time_buy > 5 else 5
                start_price = round_up_to_unit(open_last_row, close_last_row, step_price)       
                price_current = stock_data_trading.iloc[-1]['close']
                percent_first_buy = trading_config.stock_config_percent_first_buy
                logger.info(f'percent_first_buy {symbol}: {percent_first_buy}')
                number_order = trading_config.stock_config_number_pid_buy_once_time
                time_now = datetime.now(timezone)
                start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                slippage_buy = trading_config.stock_config_slippage_buy
                # Dao động cộng trừ    
                add_price_buy = trading_config.stock_config_add_price_buy
                # Get stock balance to set volume
                res_stock_balance = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
                stock_balance = res_stock_balance.get('stock_balance', {}).get('actual_vol', 0) if res_stock_balance else 0
                number_stock_existing = res_stock_balance.get('number_stock_existing', 0) if res_stock_balance else 0
                cash_balance = handle_cash_balance_service(user_name, account, request_url, session, '')
                volume_to_buy = overview_config.volume_to_buy        
                #Kiểm tra đk số cổ phiếu giới hạn, khối lượng mua còn lại, tiền mặt
                if number_stock_existing >= max_stock_existing and stock_balance == 0 :
                    logger.info(f'Lệnh mua {symbol} rơi vào trường hợp vượt quá số cổ phiếu tối đa hiện đang là {number_stock_existing}')
                elif not cash_balance:
                    logger.info(f'không có respon khi lấy số dư tiền mặt {symbol}')
                else: 
                    volume_buy_balance =  int(volume_to_buy - stock_balance)
                    volume = min(((int(volume_to_buy * percent_first_buy) + 99) // 100) * 100,(volume_buy_balance // 100) * 100)
                    buy_order_overrall_attrs = {
                        'user_account': account,
                        'stock': symbol,
                        'volume_to_buy': int(volume_to_buy),
                        'volume_set_buy': volume,
                        'level': level,
                        'start_price': round(start_price, 2),
                        "current_price": round(price_current, 2),
                        'limit_price': round(start_price - add_price_buy + slippage_buy, 2),
                        'step_price': step_price,
                        "slippage_buy": slippage_buy,
                        "add_price_buy": add_price_buy,
                        "sleeping_time_buy": int(sleeping_time_buy),                     
                        'number_order': int(number_order),
                        'start_time_order': start_time_order,
                        'percent_first_buy': int(percent_first_buy*100)
                    }

                    buy_messages = []
                    buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_OVERRAL,
                                    **buy_order_overrall_attrs })  
                    
                # Xử lý mua nhạy cảm 
                    if volume >=100 and trading_config.stock_config_is_mode_sensitive_buy:
                        sensitive_percentage = trading_config.stock_config_percent_sensitive_buy
                        logger.info(f'sensitive_percentage {symbol}: {sensitive_percentage}')
                        volume_buy_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                        logger.info(f'volume_buy_sensitive {symbol}: {volume_buy_sensitive}')
                        price_set_buy = min(start_price, price_current)
                        buy_order_attrs_send = {
                            'stock': symbol,
                            # 'price': round(float(high_last_row - add_price_buy), 2), # Giá mua tạm thời giảm so với yêu cầu thuật toán, cần sửa lại
                            'price': round(price_set_buy, 2),
                            'volume': int(volume_buy_sensitive)
                        }
                        logger.info(f'buy_order_attrs_send {symbol}: {buy_order_attrs_send}')
                        res_buy = handle_buy_service(user_name, account, request_url, symbol, session, asp_net_session, buy_order_attrs_send['price'],  buy_order_attrs_send['volume'], ref_id)
                        if res_buy:
                            is_send_order_buy = True
                            buy_order_sensitive_attrs = {
                                'stock': res_buy['symbol'],
                                'price': round(res_buy['price'], 2),
                                'volume': res_buy['volume'],
                                'status': res_buy['status'],
                            }
                            buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_DETAIL,
                                            **buy_order_sensitive_attrs })
                            volume -= int(res_buy['volume'])
                            number_order -= 1
                        else:
                            logger.info(f"Error: lệnh mua nhạy cảm handle_buy_service  của {symbol} có phản hồi là rỗng")
                    else:
                        logger.info(f'Mã {symbol} đạt khối lượng tối đa') 
                        logger.info(f'volume_to_buy {symbol}: {volume_to_buy}')
                        logger.info(f'volume_set_buy {symbol}: {volume}')
                # Chia đều phần còn lại của volume to buy
                    number_order = min(number_order, volume // 100)
                    if volume >=100:
                        for i in range(int(number_order)):
                            divisor = number_order - i
                            if i != int(number_order) - 1:
                                volume_buy = round_to_nearest_hundred(volume / divisor)
                            else:
                                volume_buy = round_to_nearest_hundred(volume)
                        #Gửi các lệnh buy
                            ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
                            price = round(start_price - add_price_buy - i*step_price, 2)
                            if volume_buy >= 100:
                                res_buy = handle_buy_service(user_name, account, request_url, symbol, session, asp_net_session, price,  volume_buy, ref_id)
                                if res_buy:
                                    is_send_order_buy = True
                                    buy_order_details_attrs = {
                                    'stock': res_buy['symbol'],
                                    'price': round(res_buy['price'], 2),
                                    'volume': res_buy['volume'],
                                    'status': res_buy['status'],
                                    }                
                                    buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_DETAIL,
                                                    **buy_order_details_attrs })                            
                            else:
                                logger.info(f"Error: lệnh mua lần thứ {i+1} hàm handle_buy_service  của {symbol} có phản hồi là rỗng") 
                            volume -= volume_buy
                    else:
                        logger.info(f'Mã {symbol} đạt khối lượng tối đa') 
                # Send telegram tổng hợp khi thực hiện đặt xong các lệnh mua
                if is_send_order_buy:
                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
                    send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_buy, **buy_attrs)             
                    send_telegram_message_batch(user, MessageTypeEnum.OVERALL, buy_messages)
                    send_telegram_message_batch(user, MessageTypeEnum.ACT, buy_messages)
        
                logger.info(f'kết thúc hàm đặt lệnh request buy {symbol}')        

            # Update buy order
            if is_send_order_buy: 
                limited_times = time_to_buy // sleeping_time_buy
                limited_price_to_buy = start_price - add_price_buy + slippage_buy
                interval_check = 10  # Kiểm tra mỗi 10 giây
                should_break_loop = False  # Flag để thoát khỏi vòng for
                for i in range(int(limited_times) - 1):
                    if should_break_loop:
                        break
                    start_sleep = time.time()
                    while time.time() - start_sleep < sleeping_time_buy:
                        connection.close()  # Close connection before sleep
                        remaining = sleeping_time_buy - (time.time() - start_sleep)
                        sleep_time = min(interval_check, remaining)
                        if sleep_time <= 0:
                            break
                        time.sleep(sleep_time)
                
                        # 🔄 Lấy lại cấu hình mới mỗi lần lặp để cập nhật cấu hình mới nhất
                        try:
                            configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                                user=user, 
                                stock_symbol=symbol
                            )
                            if configuration:
                                refreshed_overview_config = configuration.get("overview_config")
                                if refreshed_overview_config:
                                    overview_config = refreshed_overview_config
                        except Exception as e:
                            logger.info(f'Lỗi khi lấy lại cấu hình mua tay cho {symbol}: {e}')
                            connection.close()
                            # Tiếp tục dùng config cũ nếu lỗi
                
                        is_block_buy_stock = overview_config.is_block_buy
                        is_buy_hand = overview_config.is_buy_hand

                        logger.info(f'[{symbol}] Check Loop: is_block_buy={is_block_buy_stock}, is_buy_hand={is_buy_hand}')
                
                        if is_block_buy_stock:
                            logger.info(f'{symbol} đã bị chặn mua, hủy lệnh mua tay {symbol}')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đã bị chặn mua', "B")
                            # revert_status_request_trade removed here, handled in finally
                            should_break_loop = True
                            break                        
                        if not is_buy_hand:
                            logger.info(f'{symbol} Đã tắt mua tay, hủy lệnh mua tay {symbol} ngay lập tức.')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đã tắt mua tay', "B")
                            # revert_status_request_trade removed here, handled in finally
                            should_break_loop = True
                            break
                        is_time_valid_to_buy = is_valid_time_to_buy(following_config)
                        if not is_time_valid_to_buy:
                            logger.info(f'{symbol} Vượt khung giờ mua, hủy lệnh mua tay {symbol} ngay lập tức.')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đã vượt khung giờ mua', "B")
                            # revert_status_request_trade removed here, handled in finally
                            should_break_loop = True
                            break
            
                    status_buy = SignalTelegramEnum.BUY_SUCCESS
                    times_update = i + 1
                    message_update = update_buy_order(user_name, account, symbol, request_url, session, asp_net_session, "B", 
                                                        step_price, limited_price_to_buy, times_update)
                    if message_update:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                    else:
                        logger.info(f"Sửa lệnh thất bại ở lần thứ {times_update}, sẽ huỷ lệnh.")                
                        cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Sửa lệnh mua không thành công', "B")
                        # revert_status_request_trade removed here, handled in finally
                        break

                #Tổng kết các lệnh đã khớp theo symbol để send telegram
                try:
                    time.sleep(2)  # đợi backend cập nhật
                    res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'B') 
                    if res_matcheds:
                        time_now = datetime.now(timezone)
                        start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                        message_buy_matched = []
                        buy_matched_overrall_attrs = {
                            'user_account': account,
                            'stock': symbol,
                            'number_order': len(res_matcheds),
                            'start_time_order': start_time_order,
                            } 
                        message_buy_matched.append({
                            'status_signal': SignalTelegramEnum.BUY_MATCHED_OVERRAL,
                            **buy_matched_overrall_attrs
                            })
                        for order in res_matcheds:
                            buy_matched_details_attrs = {
                                'stock': order['symbol'],
                                'price': order['showPrice'],
                                'volume': order['volume'],
                                'status': order['status']
                                }
                            message_buy_matched.append({
                                'status_signal': SignalTelegramEnum.BUY_MATCHED_DETAIL,
                                **buy_matched_details_attrs
                                })
                        if message_buy_matched:
                            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_buy_matched)
                            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_buy_matched)
                    else:
                        logger.info(f'Không lấy được danh sách các lệnh đã khớp symbol: {symbol}')
                except Exception as e:
                    logger.info(f"Lỗi khi xử lý matched orders: {e}")
                    message = f'Không lấy được thông tin các lệnh mua tay đã khớp mã {symbol}'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message)
                    send_message_telegram(user, MessageTypeEnum.ACT, message)
            #Hủy tất cả các lệnh nếu còn đặt
                cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Hủy các lệnh mua còn sót lại', "B")
        except Exception as e:
            logger.error(f'FATAL ERROR in process_buy_request {symbol}: {e}', exc_info=True)
        finally:
            logger.info(f'Finalizing process_buy_request for {symbol}')
            revert_status_request_trade(user, stock_id)
    else:
        message_cancel = f'Vượt khung giờ mua mã {symbol}, hủy yêu cầu mua tay.'
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
        revert_status_request_trade(user, stock_id)

def process_sell_request(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, stock_id: str, limit_number_stocks: int, request_buy: bool, request_sell: bool, volume_sell: str, is_use_chart_action: bool):
    # Các giá trị mặc định    
    user_name = vps_account.name
    account = vps_account.account_num
    session = vps_account.vps_session_id
    request_url = api.TRADING_URL
    ref_id = f"{user_name}.I.test.{int(time.time() * 1000)}"
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    
    
    # Lấy dữ liệu đã chuẩn bị  
    trading_candle_sell = prepared["trading_candle_sell"]
    trading_candle_sell_second = prepared["trading_candle_sell_second"]
    following_candle_sell = prepared["following_candle_sell"]
    following_candle_sell_second = prepared["following_candle_sell_second"]
    trading_chart_type_sell = prepared["trading_chart_type_sell"]
    trading_chart_type_sell_second = prepared["trading_chart_type_sell_second"]
    following_chart_type_sell = prepared["following_chart_type_sell"]
    following_chart_type_sell_second = prepared["following_chart_type_sell_second"]
    trading_config = prepared["trading_config"]
    following_config = prepared["following_config"]        
    overview_config = prepared["overview_config"]
    stock = prepared["stock"]
    symbol = stock.name        
    asp_net_session = ''

    logger.info(f'Đang request sell: {symbol} với khối lượng: {volume_sell}')  

    slippage_sell = trading_config.stock_config_slippage_sell
    add_price_sell = trading_config.stock_config_add_price_sell
    is_time_valid_to_sell = is_valid_time_to_sell(following_config)
    #HANDLE SELL
    if is_time_valid_to_sell:
        try:
            update_status, update_data = ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
            if update_status != SuccessType.UPDATED_SUCCESS:
                logger.error(f'Failed to update is_trading for {symbol}: {update_data}')
                message_fail = f'⚠️ Đưa {symbol} vào danh sách đang hoạt động thất bại. Hủy yêu cầu bán tay!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_fail)
                send_message_telegram(user, MessageTypeEnum.ACT, message_fail)
                return
            # Xác định thời gian bắt đầu và thời gian kết thúc (sau 1 tiếng)
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=2)
            status_sell = SignalTelegramEnum.SELL_REQUEST_FAILED
            last_buy_check_time = None
            message_stop_sell = 'Hết thời gian của lệnh bán tay'
            price_to_start = None  # Khởi tạo giá trị mặc định để tránh lỗi khi sử dụng sau vòng lặp
            
            if not is_use_chart_action:
                logger.info(f'Xu ly lenh ban ngay {symbol}')
                # Tải dữ liệu lần 1
                vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                    stock=stock, 
                    vnindex_stock=vnindex_stock, 
                    trading_chart_type=trading_chart_type_sell, 
                    following_chart_type=following_chart_type_sell,
                )
            if stock_data_trading is None:
                logger.info('Download data không thành công, bỏ qua!')
                message_download = f'Không tải được dữ liệu mã {symbol}, hủy yêu cầu bán tay. Vui lòng thử lại sau ít phút!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                revert_status_request_trade(user, stock_id)
                return
            
            price_to_start = (stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close'])/2
            status_sell = SignalTelegramEnum.SELL_REQUEST_SUCCESS
            messages_to_sell = 'Bán ngay'
            
            time_now = datetime.now(timezone)
            start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
            sell_attrs = {
                "user_account": account,
                "platform_trading": "Smart One",
                "stock": stock.name,
                "volume": 0,
                "price": price_to_start,
                "message": messages_to_sell,
                "start_time_order": start_time_order,
            }
            send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs) 

            while is_use_chart_action and datetime.now() < end_time:
                close_old_connections()
                # Kiểm tra is_sell_hand mỗi 3 giây
                try:
                    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
                    overview_config = configuration.get("overview_config", {})
                    is_sell_hand = overview_config.is_sell_hand
                    logger.info(f'check is_sell_hand overview_config {symbol} : {is_sell_hand}')
                except Exception as e:
                    logger.error(f'Lỗi khi lấy lại cấu hình bán tay cho {symbol}: {e}')
                    connection.close()
                    time.sleep(1)
                    continue
            
                if not is_sell_hand:
                    logger.info(f'Dừng bán tay cổ phiếu {symbol} : {is_sell_hand}')
                    message_stop_sell = 'Yêu cầu dừng bán tay'
                    break  # Thoát khỏi vòng while và tiếp tục đoạn code phía sau
            
                # Kiểm tra điều kiện mua chỉ mỗi 60 giây một lần
                now = datetime.now()
                if last_buy_check_time is None or (now - last_buy_check_time).total_seconds() >= 60:
                    last_buy_check_time = now

                    # === XỬ LÝ BÁN ===
                    # Tải dữ liệu lần 1
                    vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_sell, 
                        following_chart_type=following_chart_type_sell,
                    )
                    # Tải dữ liệu lần 2
                    vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_sell_second, 
                        following_chart_type=following_chart_type_sell_second
                    )
                    if stock_data_trading is None:
                        logger.info('Download data không thành công, bỏ qua!')
                        message_download = f'Không tải được dữ liệu mã {symbol}, hủy yêu cầu bán tay. Vui lòng thử lại sau ít phút!'
                        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                        send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                        revert_status_request_trade(user, stock_id)
                        return
                    logger.info('Download data thành công!')
                    price_to_start = (
                        stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close'])/2
                
                    # 🔄 Lấy lại prepared mới mỗi lần lặp để cập nhật cấu hình mới nhất
                    try:
                        configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                            user=user, 
                            stock_symbol=symbol
                        )
                        if configuration:
                            refreshed_trading_config = configuration.get("trading_config")
                            refreshed_following_config = configuration.get("following_config")
                            refreshed_overview_config = configuration.get("overview_config")
                            refreshed_stock = configuration.get("stock")
                        
                            # Cập nhật các biến config nếu lấy được
                            if refreshed_trading_config:
                                trading_config = refreshed_trading_config
                                trading_candle_sell = getattr(getattr(trading_config, "candle_sell", None), "candle_sell", "M5")
                                trading_candle_sell_second = getattr(getattr(trading_config, "candle_sell_second", None), "candle_sell", "M5")
                                trading_chart_type_sell = getattr(CandleEnum, trading_candle_sell, CandleEnum.M5)
                                trading_chart_type_sell_second = getattr(CandleEnum, trading_candle_sell_second, CandleEnum.M5)
                            if refreshed_following_config:
                                following_config = refreshed_following_config
                                following_candle_sell = getattr(getattr(following_config, "candle_sell", None), "candle_sell", "D1")
                                following_candle_sell_second = getattr(getattr(following_config, "candle_sell_second", None), "candle_sell", "D1")
                                following_chart_type_sell = getattr(CandleEnum, following_candle_sell, CandleEnum.D1)
                                following_chart_type_sell_second = getattr(CandleEnum, following_candle_sell_second, CandleEnum.D1)
                            if refreshed_overview_config:
                                overview_config = refreshed_overview_config
                            if refreshed_stock:
                                stock = refreshed_stock
                    except Exception as e:
                        logger.info(f'Lỗi khi lấy lại cấu hình cho {symbol}: {e}')
                        connection.close()
                        # Tiếp tục dùng config cũ nếu lỗi
                
                    is_sell, sell_reason = should_sell_trading(
                        trading_config=trading_config,
                        data_trading_df=stock_data_trading,
                        config_type='stock_config',
                        data_trading_df_second=stock_data_trading_second
                    )
                    if is_sell:
                        status_sell = SignalTelegramEnum.SELL_REQUEST_SUCCESS
                    messages_to_sell = render_message(
                        sell_reason, trading_chart_value=trading_candle_sell, trading_chart_value_second=trading_candle_sell_second, following_chart_type=following_candle_sell, following_chart_type_second=following_candle_sell_second
                    )

                    time_now = datetime.now(timezone)
                    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                    sell_attrs = {
                        "user_account": account,
                        "platform_trading": "Smart One",
                        "stock": stock.name,
                        "volume": 0,
                        "price": price_to_start,
                        "message": messages_to_sell,
                        "start_time_order": start_time_order,
                    }
                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)    
                
                    if status_sell == SignalTelegramEnum.SELL_REQUEST_SUCCESS:              
                        logger.info('Dừng vòng lặp do  điều kiện bán thỏa mãn.')
                        break 

                for _ in range(3):
                    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
                    overview_config = configuration.get("overview_config", {})
                    if not overview_config.is_sell_hand:
                        logger.info(f"Phát hiện tắt bán tay trong lúc chờ đợi, thoát vòng lặp.")
                        break
                    time.sleep(1) 

            if status_sell == SignalTelegramEnum.SELL_REQUEST_FAILED:
                logger.info('Dừng vòng lặp do vượt thời gian hoặc yêu cầu ngừng bán tay.')
                revert_status_request_trade(user, stock_id)
                # Nếu price_to_start chưa được khởi tạo, download data một lần nữa để lấy giá
                if price_to_start is None:
                    try:
                        vnindex_data_trading_temp, vnindex_data_following_temp, stock_data_trading_temp, stock_data_following_temp = download_data(
                            stock=stock, 
                            vnindex_stock=vnindex_stock, 
                            trading_chart_type=trading_chart_type_sell, 
                            following_chart_type=following_chart_type_sell,
                        )
                        if stock_data_trading_temp is not None and len(stock_data_trading_temp) > 0:
                            price_to_start = (stock_data_trading_temp.iloc[-1]['open'] + stock_data_trading_temp.iloc[-1]['close']) / 2
                        else:
                            price_to_start = 0  # Giá trị mặc định nếu không lấy được
                    except Exception as e:
                        logger.error(f"Lỗi khi download data để lấy price_to_start: {e}")
                        price_to_start = 0  # Giá trị mặc định nếu có lỗi
                time_now = datetime.now(timezone)
                start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                sell_attrs = {
                    "user_account": account,
                    "platform_trading": "Smart One",
                    "stock": stock.name,
                    "volume": 0,
                    "price": price_to_start if price_to_start is not None else 0,
                    "message": message_stop_sell,
                    "start_time_order": start_time_order,
                }
                try:
                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)
                except Exception as e:
                    logger.info(f"❌ Lỗi khi gửi tin nhắn: {e}") 
            is_send_order_sell = False   
            if status_sell == SignalTelegramEnum.SELL_REQUEST_SUCCESS:
                logger.info(f'bắt đầu đặt lệnh sell request {symbol}')        
                timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                last_row = stock_data_trading.iloc[-1]
                open_last_row = last_row['open']
                close_last_row = last_row['close']
                low_last_row = last_row['low']
                high_last_row = last_row['high']
                step_price = trading_config.stock_config_slippage_volume_sell_per_pid
                # logger.info(f'check step_price stock {symbol}: ', step_price)
                sleeping_time_sell= trading_config.stock_config_time_update_pid_sell
            
                sleeping_time_sell = sleeping_time_sell if sleeping_time_sell > 5 else 5
                time_to_sell = trading_config.stock_config_time_to_sell
                time_to_sell = time_to_sell if time_to_sell >= 30 else 30
                start_price = round_up_to_unit(open_last_row, close_last_row, step_price)       
                price_current = stock_data_trading.iloc[-1]['close']
                number_order = trading_config.stock_config_number_pid_sell_once_time 
                start_time_order = datetime.now(timezone).strftime("%H:%M:%S ngày %d-%m-%Y")
                slippage_sell = trading_config.stock_config_slippage_sell
            # Dao động cộng trừ     
                add_price_sell = trading_config.stock_config_add_price_sell

            # Get stock balance to set volume
                res_stock_balance = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
                stock_balance = res_stock_balance.get('stock_balance', {}).get('actual_vol', 0) if res_stock_balance else 0
                stock_balance = res_stock_balance.get('stock_balance', {}).get('available_vol', 0) if res_stock_balance else 0
                ceil_price = res_stock_balance.get('stock_balance', {}).get('ceil_price', 0) if res_stock_balance else 0  
                volume_balance = (stock_balance // 100) * 100
                half = volume_balance / 2
                volume = int(volume_balance) if volume_sell == 'all' else int(half + 50) if half % 100 == 50 else int(half)
                sell_order_overrall_attrs = {
                    'user_account': account,
                    'stock': symbol,
                    'volume': int(volume),
                    'start_price': round(start_price, 2),
                    "current_price": round(price_current, 2),
                    'step_price': step_price,
                    "slippage_sell": slippage_sell,
                    "add_price_sell": add_price_sell,
                    "sleeping_time_sell": int(sleeping_time_sell),
                    'limit_price': round(start_price + add_price_sell - slippage_sell, 2),  
                    'number_order': int(number_order),
                    'start_time_order': start_time_order
                }
                sell_messages = []
                sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_OVERRAL,
                                    **sell_order_overrall_attrs })
            
                if volume >= 100:
                # Xử lý bán nhạy cảm 
                    if trading_config.stock_config_is_mode_sensitive_sell:
                        sensitive_percentage = trading_config.stock_config_percent_sensitive_sell
                        volume_sell_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                        volume_sell_sensitive = volume_sell_sensitive if volume_sell_sensitive >= 100 else 100
                        price_set_sell = max(start_price, price_current)
                        sell_order_attrs_send = {
                            'stock': symbol,
                            # 'price': round(float(low_last_row + add_price_sell), 2) if round(float(low_last_row + add_price_sell), 2) < ceil_price else round(ceil_price, 2) , 
                            'price': round(price_set_sell, 2),
                            'volume': int(volume_sell_sensitive)
                        }
                        res_sell = handle_sell_service(user_name, account, request_url, symbol, session, asp_net_session, sell_order_attrs_send['price'],  sell_order_attrs_send['volume'], ref_id)
                        if res_sell:
                            is_send_order_sell = True
                            sell_order_sensitive_attrs = {
                                'stock': res_sell['symbol'],
                                'price': round(res_sell['price'], 2),
                                'volume': res_sell['volume'],
                                'status': res_sell['status'],
                            }
                            sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_DETAIL,
                                                **sell_order_sensitive_attrs })
                            volume -= int(res_sell['volume'])
                            number_order -= 1
                        else:
                            logger.info(f"Error: lệnh bán nhạy cảm handle_sell_service  của {symbol} phản hồi là rỗng") 
                # Chia đều phần còn lại của volume to sell
                    if volume >= 100:
                        number_order = min(number_order, volume // 100)
                        for i in range(int(number_order)):
                            divisor = number_order - i
                            if i != int(number_order) - 1:
                                volume_sell = round_to_nearest_hundred(volume / divisor)
                            else:
                                volume_sell = round_to_nearest_hundred(volume / divisor) if volume % 100 != 0 else int(volume)
                            volume -= volume_sell
                            #Gửi các lệnh sell
                            ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
                            price = round(start_price + add_price_sell + i*step_price, 2) if round(start_price + add_price_sell + i*step_price, 2) < ceil_price else round(ceil_price, 2)
                            if volume_sell >= 100:
                                res_sell = handle_sell_service(user_name, account, request_url, symbol, session, asp_net_session, price,  volume_sell, ref_id)
                                if res_sell:
                                    is_send_order_sell = True
                                    sell_order_details_attrs = {
                                        'stock': res_sell['symbol'],
                                        'price': round(res_sell['price'], 2),
                                        'volume': res_sell['volume'],
                                        'status': res_sell['status'],
                                    }                
                                    sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_DETAIL,
                                                        **sell_order_details_attrs })
                            else:
                                logger.info(f"Error: lệnh bán lần thứ {i+1} hàm handle_sell_service  của {symbol} có phản hồi là rỗng") 
                # Send telegram tổng hợp khi thực hiện đặt xong các lệnh bán
                    if is_send_order_sell:
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)
                        send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_sell, **sell_attrs)
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, sell_messages)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, sell_messages) 
                logger.info('kết thúc hàm đặt lệnh sell')     
        
            if is_send_order_sell:
                limited_times = time_to_sell // sleeping_time_sell
                limited_price_to_sell = start_price + add_price_sell - slippage_sell
                logger.info(f'check limit_price_to_sell {symbol}: {limited_price_to_sell}')
                interval_check = 10  # Kiểm tra mỗi 10 giây
                should_break_loop = False  # Flag để thoát khỏi vòng for
            
                for i in range(int(limited_times) - 1):
                    if should_break_loop:
                        break
                    start_sleep = time.time()
                    while time.time() - start_sleep < sleeping_time_sell:
                        connection.close()  # Close connection before sleep
                        remaining = sleeping_time_sell - (time.time() - start_sleep)
                        sleep_time = min(interval_check, remaining)
                        if sleep_time <= 0:
                            break
                        time.sleep(sleep_time)
                    
                        # 🔄 Lấy lại cấu hình mới mỗi lần lặp để cập nhật cấu hình mới nhất
                        try:
                            configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                                user=user, 
                                stock_symbol=symbol
                            )
                            if configuration:
                                refreshed_overview_config = configuration.get("overview_config")
                                if refreshed_overview_config:
                                    overview_config = refreshed_overview_config
                        except Exception as e:
                            logger.info(f'Lỗi khi lấy lại cấu hình bán tay cho {symbol}: {e}')
                            connection.close()
                            # Tiếp tục dùng config cũ nếu lỗi
                    
                        is_block_sell_stock = overview_config.is_block_sell
                        is_sell_hand = overview_config.is_sell_hand
                        logger.info(f'[{symbol}] Check Loop Sell: is_block_sell={is_block_sell_stock}, is_sell_hand={is_sell_hand}')

                        if is_block_sell_stock:
                            logger.info(f'{symbol} đã bị chặn bán, hủy lệnh bán tay {symbol}')
                            cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Đã bị chặn bán', "S")
                            should_break_loop = True
                            break
                    
                        if not is_sell_hand:
                            logger.info(f'{symbol} Đã tắt bán tay, hủy lệnh bán tay {symbol} ngay lập tức.')
                            cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Đã tắt bán tay', "S")
                            should_break_loop = True
                            break
                        is_time_valid_to_sell  = is_valid_time_to_sell(following_config)
                        if not is_time_valid_to_sell :
                            logger.info(f'{symbol} Đã vượt khung giờ bán, hủy lệnh bán tay {symbol} ngay lập tức.')
                            cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Đã vượt khung giờ bán', "S")
                            should_break_loop = True
                            break
                
                    status_sell = SignalTelegramEnum.SELL_SUCCESS
                    times_update = i + 1
                    message_update = update_sell_order(user_name, account, symbol, request_url, session, asp_net_session, "S", step_price, limited_price_to_sell, times_update)
                    if message_update:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                    else:
                        cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lỗi không sửa được lệnh bán tay', "S")
                        break 

                #Tổng kết các lệnh đã khớp theo symbol để send telegram 
                try:          
                    res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'S')
                    if res_matcheds:
                        logger.info(f'danh sách các lệnh bán {symbol} đã khớp: {res_matcheds}')
                        message_sell_matched = []
                        sell_matched_overrall_attrs = {
                            'user_account': account,
                            'stock': symbol,
                            'number_order': len(res_matcheds),
                            } 
                        message_sell_matched.append({
                            'status_signal': SignalTelegramEnum.SELL_MATCHED_OVERRAL,
                            **sell_matched_overrall_attrs
                            })
                        for order in res_matcheds:
                            sell_matched_details_attrs = {
                                'stock': order['symbol'],
                                'price': order['showPrice'],
                                'volume': order['volume'],
                                'status': order['status']
                                }
                            message_sell_matched.append({
                                'status_signal': SignalTelegramEnum.SELL_MATCHED_DETAIL,
                                **sell_matched_details_attrs
                                })
                        if message_sell_matched:
                            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_sell_matched)
                            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_sell_matched)

                except Exception as e:
                    logger.info(f"Lỗi khi xử lý matched orders: {e}")
                    message = f'Không lấy được thông tin các lệnh bán tay đã khớp mã {symbol}'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message)
                    send_message_telegram(user, MessageTypeEnum.ACT, message)
            #Hủy tất cả các lệnh nếu còn đặt
                cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Hết thời gian đặt lệnh bán tay', "S")
        finally:
            logger.info(f'Finalizing process_sell_request for {symbol}')
            revert_status_request_trade(user, stock_id)
    else:
        message_cancel = f'Vượt khung giờ bán mã {symbol}, hủy yêu cầu bán tay.'
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
        revert_status_request_trade(user, stock_id)

def process_trading(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, percent_buy_trade: float):
    # Khởi tạo stock_id = None để tránh lỗi nếu exception xảy ra trước khi khởi tạo
    stock_id = None
    try:        
        # Các giá trị mặc định
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        user_name = vps_account.name
        account = vps_account.account_num
        session = vps_account.vps_session_id
        request_url = api.TRADING_URL
        ref_id = f"{user_name}.I.test.{int(time.time() * 1000)}"
        
        # Lấy tên luồng hiện tại
        current_thread_name = threading.current_thread().name
        # Lấy dữ liệu đã chuẩn bị  
        trading_candle = prepared["trading_candle"]
        trading_candle_second = prepared["trading_candle_second"]
        trading_candle_sell = prepared["trading_candle_sell"]
        trading_candle_sell_second = prepared["trading_candle_sell_second"]
        following_candle = prepared["following_candle"]
        following_candle_second = prepared["following_candle_second"]
        following_candle_sell = prepared["following_candle_sell"]
        following_candle_sell_second = prepared["following_candle_sell_second"]
        trading_chart_type = prepared["trading_chart_type"]
        trading_chart_type_second = prepared["trading_chart_type_second"]
        trading_chart_type_sell = prepared["trading_chart_type_sell"]
        trading_chart_type_sell_second = prepared["trading_chart_type_sell_second"]
        following_chart_type = prepared["following_chart_type"]
        following_chart_type_second = prepared["following_chart_type_second"]
        following_chart_type_sell = prepared["following_chart_type_sell"]
        following_chart_type_sell_second = prepared["following_chart_type_sell_second"]
        trading_config = prepared["trading_config"]
        following_config = prepared["following_config"]        
        overview_config = prepared["overview_config"]
        stock = prepared["stock"]
        symbol = stock.name        
        asp_net_session = ''
        percent_first_buy = trading_config.stock_config_percent_first_buy
        
        logger.info(f'Bắt đầu process_trading: {symbol}')
        is_block_buy_stock = overview_config.is_block_buy
        is_block_sell_stock = overview_config.is_block_sell
        stock_id = trading_config.stock_id
        # Get stock balance 
        res_stock_balance = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
        stock_balance = res_stock_balance.get('stock_balance', {}).get('actual_vol', 0) if res_stock_balance else 0
        volume_balance_trade = res_stock_balance.get('stock_balance', {}).get('available_vol', 0) if res_stock_balance else 0
        ceil_price = res_stock_balance.get('stock_balance', {}).get('ceil_price', 0) if res_stock_balance else 0
        symbols_existing = res_stock_balance.get('symbols_existing', []) if res_stock_balance else []
        cash_balance = handle_cash_balance_service(user_name, account, request_url, session, '')
        cash_available = cash_balance['cash_available']

        # === EARLY LOCKING ===
        # Cố gắng acquire lock ngay từ đầu để tránh race condition và tính toán vô ích
        lock_status, lock_data = ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
        if lock_status != SuccessType.UPDATED_SUCCESS:
            logger.warning(f"⚠️ Không thể chiếm quyền giao dịch (lock) cho {symbol}. Có thể tiến trình khác đang chạy hoặc đã bị khóa.")
            # Không làm gì thêm, return để kết thúc task này
            return

    #HANDLE BUY
        is_time_valid_to_buy = is_valid_time_to_buy(following_config)
        if not is_block_buy_stock and is_time_valid_to_buy:
            # Tải dữ liệu lần 1
            vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type, 
                following_chart_type=following_chart_type
            )
             # Tải dữ liệu lần 2
            vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type_second, 
                following_chart_type=following_chart_type_second
            )
            sales_data = download_sales_volume(symbol=symbol)
            if sales_data is None:
                logger.info(f'❌ Download sales_data cho {symbol} không thành công sau 3 lần thử!')
                message_download = f'⚠️ Download sales_data to buy symbol {symbol} failed after 3 attempts. Skipping!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)  
                return
            elif stock_data_following is None:
                logger.info(f'❌ Download following_data cho {symbol} không thành công!')
                message_download = f'⚠️ Download following to buy symbol {symbol} failed. Skipping!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)  
                return               
            def safe_int(val):
                try:
                    return int(val) if val is not None else 0
                except (ValueError, TypeError):
                    return 0   
            floor_price = sales_data.get('floor_price')
            buyForeignQtty = safe_int(sales_data.get('buyForeignQtty'))
            sellForeignQtty = safe_int(sales_data.get('sellForeignQtty'))
            total_foreign = buyForeignQtty + sellForeignQtty
            if total_foreign > 0:
                value_buy_foreign = round((buyForeignQtty / total_foreign) * 100, 2)
            else:
                value_buy_foreign = 0

            # Gán cho 3 dòng cuối
            stock_data_following.loc[stock_data_following.index[-3:], 'buy_foreign'] = value_buy_foreign          
            stock_data_following.loc[stock_data_following.index[-3:], 'volume_trade'] = percent_buy_trade
            stock_data_following_second.loc[stock_data_following_second.index[-3:], 'buy_foreign'] = value_buy_foreign          
            is_use_vnindex_following = following_config.is_use_vnindex_config
            logger.info(f'bắt đầu hàm should buy {symbol}')            
            is_buy_following, is_buy, buy_reason = should_buy(
                        trading_config = trading_config,
                        following_config = following_config,
                        data_following_df = stock_data_following,
                        data_following_df_second = stock_data_following_second,
                        data_trading_df = stock_data_trading,            
                        data_trading_df_second = stock_data_trading_second,            
                        config_type = 'stock_config'
                    )  
                    
            messages_to_buy_vnindex = ''
            if is_use_vnindex_following:
                is_buy_vnindex, buy_reason_vnindex = should_buy_following(
                    following_config = following_config,
                    data_following_df = vnindex_data_following,
                    config_type = 'vnindex_config',
                    data_following_df_second = vnindex_data_following_second
                )
                messages_to_buy_vnindex = render_message(
                buy_reason_vnindex, trading_chart_value=trading_candle, following_chart_type=following_candle, following_chart_type_second=following_candle_second)
                # logger.info(f'check buy_reason_vnindex {symbol}: {buy_reason_vnindex}') 
                if not is_buy_vnindex:
                    is_buy = is_buy_vnindex  

            logger.info(f'check is_buy {symbol}: {is_buy}')
            # if symbol in ['PC1', 'BVH']:
            #     logger.info(f'check buy_reason {symbol}: {buy_reason}')     

            number_order = trading_config.stock_config_number_pid_buy_once_time
            if is_buy:
                status_buy = SignalTelegramEnum.BUY_SUCCESS
            else:
                status_buy = SignalTelegramEnum.BUY_FAILED
            messages_to_buy = render_message(
                buy_reason, trading_chart_value=trading_candle, trading_chart_value_second=trading_candle_second, following_chart_type=following_candle, following_chart_type_second=following_candle_second)
           
            price_to_start = (stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close'])/2
            price_current = stock_data_trading.iloc[-1]['close']   
            level = overview_config.level         
            time_now = datetime.now(timezone)
            start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
            buy_attrs = {
                "user_account": account,
                "platform_trading": "Smart One",
                "stock": stock.name,
                "level": level,
                "current_price": round(price_current, 2),
                "price": price_to_start,
                "times": 'first',
                "message": messages_to_buy,
                "message_vnindex": messages_to_buy_vnindex,
                "start_time_order": start_time_order,
            }
            if is_buy_following and not is_buy:
                send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
            
            # if symbol in ['PC1', 'BVH']:
            #     send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
            is_send_order_buy = False   
            if status_buy == SignalTelegramEnum.BUY_SUCCESS:
                logger.info(f'bắt đầu hàm đặt lệnh buy {symbol} (Đã có lock từ đầu)')                
                
                # Vì đã lock từ đầu hàm, nên ở đây ta coi như update success
                is_update_success = True
                
                # (Đã xóa đoạn code update_is_trading_configuration cũ ở đây để tránh dư thừa/lỗi)
                
                if not is_update_success:
                    # Logic cũ (giữ lại 1 phần cấu trúc nếu cần, nhưng thực tế is_update_success luôn True ở đây)
                    logger.error(f"⛔ Logic Error: is_update_success should be True.")
                    send_message_telegram(user, MessageTypeEnum.OVERALL, "Internal Error in Locking Logic")

                    send_message_telegram(user, MessageTypeEnum.ACT, message_fail)
                    is_send_order_buy = False # Skip the buying part
                else: 
                    last_row = stock_data_trading.iloc[-1]
                    open_last_row = last_row['open'] 
                    close_last_row = last_row['close']
                    low_last_row = last_row['low']            
                    high_last_row = last_row['high']
                    step_price = trading_config.stock_config_slippage_volume_buy_per_pid
                    time_to_buy = trading_config.stock_config_time_to_buy
                    time_to_buy = time_to_buy if time_to_buy > 30 else 30
                    sleeping_time_buy = trading_config.stock_config_time_update_pid_buy
                    sleeping_time_buy = sleeping_time_buy if sleeping_time_buy > 5 else 5
                    start_price = round_up_to_unit(open_last_row, close_last_row, step_price)
                    number_order = trading_config.stock_config_number_pid_buy_once_time
                    slippage_buy = trading_config.stock_config_slippage_buy
                    # Dao động cộng trừ    
                    add_price_buy = trading_config.stock_config_add_price_buy
                    volume_to_buy = overview_config.volume_to_buy                
                    volume_buy_balance =  int(volume_to_buy - stock_balance)
                    volume = min(((int(volume_to_buy * percent_first_buy) + 99) // 100) * 100,(volume_buy_balance // 100) * 100)
                    if cash_available < volume*start_price:
                        logger.info('roi vao truong hop khong du tien mua theo yeu cau nen mua het so tien con lai')
                        volume = cash_available/start_price
                        volume = int(volume // 100 * 100)
                    buy_order_overrall_attrs = {
                        'user_account': account,
                        'stock': symbol,
                        'volume_to_buy': int(volume_to_buy),
                        'volume_set_buy': int(volume),
                        'level': level,
                        'start_price': round(start_price, 2),
                        'limit_price': round(start_price - add_price_buy + slippage_buy, 2),
                        "current_price": round(price_current, 2),
                        'step_price': step_price,
                        "slippage_buy": slippage_buy,
                        "add_price_buy": add_price_buy, 
                        "sleeping_time_buy": int(sleeping_time_buy),                   
                        'number_order': int(number_order),
                        'start_time_order': start_time_order,
                        'percent_first_buy': int(percent_first_buy*100)
                    }
                    buy_messages = []
                    buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_OVERRAL,
                                    **buy_order_overrall_attrs })  
                            
                    # Xử lý mua nhạy cảm 
                    if volume >=100 and trading_config.stock_config_is_mode_sensitive_buy:
                        sensitive_percentage = trading_config.stock_config_percent_sensitive_buy
                        volume_buy_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                        price_set_buy = min(start_price, price_current)
                        buy_order_attrs_send = {
                            'stock': symbol,
                            # 'price': round(float(high_last_row - add_price_buy), 2) if round(float(high_last_row - add_price_buy), 2) > floor_price else round(floor_price, 2),
                            'price': round(price_set_buy, 2),
                            'volume': int(volume_buy_sensitive)
                        }
                        res_buy = handle_buy_service(user_name, account, request_url, symbol, session, asp_net_session, buy_order_attrs_send['price'],  buy_order_attrs_send['volume'], ref_id)
                        if res_buy:
                            is_send_order_buy = True
                            buy_order_sensitive_attrs = {
                                'stock': res_buy['symbol'],
                                'price': round(res_buy['price'], 2),
                                'volume': res_buy['volume'],
                                'status': res_buy['status'],
                            }
                            buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_DETAIL,
                                            **buy_order_sensitive_attrs })
                            volume -= int(res_buy['volume'])
                            number_order -= 1
                        else:
                            logger.info(f"Lệnh mua nhạy cảm handle_buy_service  của {symbol} có phản hồi là rỗng") 
                    # Chia đều phần còn lại của volume to buy
                    number_order = min(number_order, volume // 100)
                    if volume >=100:
                        for i in range(int(number_order)):
                            divisor = number_order - i
                            if i != int(number_order) - 1:
                                volume_buy = round_to_nearest_hundred(volume / divisor)
                            else:
                                volume_buy = round_to_nearest_hundred(volume)
                        #Gửi các lệnh buy
                            ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
                            price = round(start_price - add_price_buy - i*step_price, 2) if round(start_price - add_price_buy - i*step_price, 2) > floor_price else round(floor_price, 2)
                            if volume_buy >= 100:
                                res_buy = handle_buy_service(user_name, account, request_url, symbol, session, asp_net_session, price,  volume_buy, ref_id)
                                if res_buy:
                                    is_send_order_buy = True
                                    buy_order_details_attrs = {
                                    'stock': res_buy['symbol'],
                                    'price': round(res_buy['price'], 2),
                                    'volume': res_buy['volume'],
                                    'status': res_buy['status'],
                                    }                
                                    buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_DETAIL,
                                                    **buy_order_details_attrs })                            
                            else:
                                logger.info(f"Error: lệnh mua lần thứ {i+1} hàm handle_buy_service  của {symbol} có phản hồi là rỗng") 
                            volume -= volume_buy  
            
                    # Send telegram tổng hợp khi thực hiện đặt xong các lệnh mua
                    if is_send_order_buy:                    
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)              
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, buy_messages)
                    # Send telegram hành động
                        send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_buy, **buy_attrs)              
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, buy_messages)
                    # logger.info(f'kết thúc hàm đặt lệnh buy {symbol}')          
            
            # Update buy order
            if is_send_order_buy:                  
                limited_times = time_to_buy // sleeping_time_buy
                limited_price_to_buy = start_price - add_price_buy + slippage_buy  
                interval_check = 10  # kiểm tra mỗi 10 giây
                should_break_loop = False  # Flag để thoát khỏi vòng for
                for i in range(int(limited_times) - 1):
                    if should_break_loop:
                        break
                    start_sleep = time.time()
                    while time.time() - start_sleep < sleeping_time_buy:
                        connection.close()

                        remaining = sleeping_time_buy - (time.time() - start_sleep)
                        sleep_time = min(interval_check, remaining)

                        if sleep_time <= 0:
                            break
                        
                        time.sleep(sleep_time)
                        
                        # 🔄 Lấy lại prepared mới mỗi lần lặp để cập nhật cấu hình mới nhất
                        try:
                            configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                                user=user, 
                                stock_symbol=symbol
                            )
                            if configuration:
                                refreshed_trading_config = configuration.get("trading_config")
                                refreshed_following_config = configuration.get("following_config")
                                refreshed_overview_config = configuration.get("overview_config")
                                refreshed_stock = configuration.get("stock")
                                
                                # Cập nhật các biến config nếu lấy được
                                if refreshed_trading_config:
                                    trading_config = refreshed_trading_config
                                    trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
                                    trading_candle_second = getattr(getattr(trading_config, "candle_second", None), "candle", "M5")
                                    trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
                                    trading_chart_type_second = getattr(CandleEnum, trading_candle_second, CandleEnum.M5)
                                if refreshed_following_config:
                                    following_config = refreshed_following_config
                                    following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
                                    following_candle_second = getattr(getattr(following_config, "candle_second", None), "candle", "D1")
                                    following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
                                    following_chart_type_second = getattr(CandleEnum, following_candle_second, CandleEnum.D1)
                                if refreshed_overview_config:
                                    overview_config = refreshed_overview_config
                                if refreshed_stock:
                                    stock = refreshed_stock
                        except Exception as e:
                            logger.info(f'Lỗi khi lấy lại cấu hình cho {symbol}: {e}')
                            connection.close()
                            # Tiếp tục dùng config cũ nếu lỗi
                        is_block_buy_stock = overview_config.is_block_buy
                        if is_block_buy_stock:
                            logger.info(f'{symbol} đã bị chặn mua, hủy lệnh mua {symbol}')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đã bị chặn mua', "B")
                            should_break_loop = True
                            break
                        is_time_valid_to_buy = is_valid_time_to_buy(following_config)
                        if not is_time_valid_to_buy:
                            logger.info(f'{symbol} đã vượt khung giờ mua, hủy lệnh mua {symbol}')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đã vượt khung giờ mua', "B")
                            should_break_loop = True
                            break
                        res_stock = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
                        number_stock_existing = res_stock.get('number_stock_existing', 0) if res_stock else 0
                        symbols_existing = res_stock.get('symbols_existing', []) if res_stock else []
                        if number_stock_existing >= vps_account.limit_number_stocks and symbol not in symbols_existing:
                            logger.info(f'Vượt giới hạn cổ phiếu tối đa, hủy lệnh {symbol}')
                            message_cancel = f'Vượt giới hạn cổ phiếu tối đa, hủy lệnh mua {symbol}'
                            send_message_telegram(user, MessageTypeEnum.OVERALL, message_cancel)
                            send_message_telegram(user, MessageTypeEnum.ACT, message_cancel)                            
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Vượt giới hạn cổ phiếu tối đa', "B")
                            should_break_loop = True
                            break
                        # --- Tải dữ liệu lần 1 ---
                        vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                            stock=stock, 
                            vnindex_stock=vnindex_stock, 
                            trading_chart_type=trading_chart_type, 
                            following_chart_type=following_chart_type
                        )
                        # Tải dữ liệu lần 2
                        vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                            stock=stock, 
                            vnindex_stock=vnindex_stock, 
                            trading_chart_type=trading_chart_type_second, 
                            following_chart_type=following_chart_type_second
                        )
                        sales_data = download_sales_volume(symbol=symbol)
                        if sales_data is None or stock_data_following is None:
                            logger.info(f'❌ Không tải được dữ liệu cho {symbol}, bỏ qua vòng này.')
                            continue
                        
                        def safe_int(val):
                            try:
                                return int(val) if val is not None else 0
                            except (ValueError, TypeError):
                                return 0   
                        
                        floor_price = sales_data.get('floor_price')
                        buyForeignQtty = safe_int(sales_data.get('buyForeignQtty'))
                        sellForeignQtty = safe_int(sales_data.get('sellForeignQtty'))
                        total_foreign = buyForeignQtty + sellForeignQtty
                        value_buy_foreign = round((buyForeignQtty / total_foreign) * 100, 2) if total_foreign > 0 else 0

                        stock_data_following.loc[stock_data_following.index[-3:], 'buy_foreign'] = value_buy_foreign
                        stock_data_following.loc[stock_data_following.index[-3:], 'volume_trade'] = percent_buy_trade
                        stock_data_following_second.loc[stock_data_following_second.index[-3:], 'buy_foreign'] = value_buy_foreign
                        is_use_vnindex_following = following_config.is_use_vnindex_config
                        is_buy, reason_buy = should_buy_following(following_config, stock_data_following, 'stock_config', stock_data_following_second) 
                        messages_to_cancel_update = render_message(
                            reason_buy, trading_chart_value=trading_candle, trading_chart_value_second=trading_candle_second, following_chart_type=following_candle, following_chart_type_second=following_candle_second) 
                        messages_to_cancel_update_vnindex = ''                  
                        if is_use_vnindex_following:
                            is_buy_vnindex, reason_buy_vnindex = should_buy_following(following_config, vnindex_data_following, 'vnindex_config', vnindex_data_following_second)
                            logger.info(f'⏱ Kiểm tra {interval_check}s - is_buy_vnindex {symbol}: {is_buy_vnindex}')
                            logger.info(f'⏱ Kiểm tra {interval_check}s - reason_buy_vnindex {symbol}: {reason_buy_vnindex}')
                            messages_to_cancel_update_vnindex = render_message(
                                reason_buy_vnindex, trading_chart_value=trading_candle, trading_chart_value_second=trading_candle_second, following_chart_type=following_candle, following_chart_type_second=following_candle_second)
                            if not is_buy_vnindex:
                                is_buy = False

                        logger.info(f'⏱ Kiểm tra {interval_check}s - is_buy {symbol}: {is_buy}')
                        logger.info(f'⏱ Kiểm tra {interval_check}s - reason_buy {symbol}: {reason_buy}')
                        
                        if not is_buy:                            
                            # Xây dựng reason với f-string và xử lý trường hợp rỗng
                            reason_parts = []
                            if messages_to_cancel_update_vnindex:
                                reason_parts.append(f"- **Lí do VNINDEX:** {messages_to_cancel_update_vnindex}")
                            if messages_to_cancel_update:
                                reason_parts.append(f"- **Lí do STOCK:**{messages_to_cancel_update}")
                            
                            # Format với xuống dòng và thụt lề đúng cách (sau "Lí do:" sẽ xuống dòng)
                            if reason_parts:
                                reason_cancel_update = "\n    " + "\n    ".join(reason_parts)
                            else:
                                reason_cancel_update = "\n    Không có lý do cụ thể"
                            
                            logger.info(f'⚠️ Điều kiện mua không còn thỏa mãn, hủy lệnh {symbol} ngay!')
                            cancel_buy_order(user, user_name, account, symbol, request_url, session, reason_cancel_update, "B")
                            should_break_loop = True
                            break  # thoát vòng kiểm tra, không update nữa
                    
                    times_update = i + 1
                    message_update = update_buy_order(
                        user_name, account, symbol, request_url, session, asp_net_session, "B",
                        step_price, limited_price_to_buy, times_update
                    )
                    if message_update:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                    else:
                        break

                #Tổng kết các lệnh đã khớp theo symbol để send telegram   
                res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'B') 
                if res_matcheds:
                    logger.info(f'danh sách các lệnh mua {symbol} đã khớp: {res_matcheds}')
                    time_now = datetime.now(timezone)
                    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                    message_buy_matched = []
                    buy_matched_overrall_attrs = {
                        'user_account': account,
                        'stock': symbol,
                        'number_order': len(res_matcheds),
                        'start_time_order': start_time_order,
                        } 
                    message_buy_matched.append({
                        'status_signal': SignalTelegramEnum.BUY_MATCHED_OVERRAL,
                        **buy_matched_overrall_attrs
                        })
                    for order in res_matcheds:
                        buy_matched_details_attrs = {
                            'stock': order['symbol'],
                            'price': order['showPrice'],
                            'volume': order['volume'],
                            'status': order['status']
                            }
                        message_buy_matched.append({
                            'status_signal': SignalTelegramEnum.BUY_MATCHED_DETAIL,
                            **buy_matched_details_attrs
                            })
                    if message_buy_matched:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_buy_matched)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_buy_matched)
                else:
                    message_buy_matched_fail = f'Không lấy được danh sách đã khớp lệnh của mã {symbol } từ sàn.'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message_buy_matched_fail)
                    send_message_telegram(user, MessageTypeEnum.ACT, message_buy_matched_fail)
                    cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Đảm bảo hết lệnh còn đặt khi kết thúc mỗi vòng mua', "B")
                
                # Mở chốt lãi lần 1 và lần 2
                logger.info('Tiến hành mở chốt lãi lần 1 và lần 2') 
                ConfigurationServices.update_all_take_profit_flags_true(user, stock_id)


    #HANDLE SELL
        is_time_valid_to_sell  = is_valid_time_to_sell(following_config)
        if not is_block_sell_stock and is_time_valid_to_sell  and symbol in symbols_existing and volume_balance_trade > 0:
            logger.info(f'bắt đầu hàm kiểm tra thực hiện sell {symbol}')
            # Handle take profit
            volume_balance = (volume_balance_trade // 100) * 100
            use_take_profit_first_part = trading_config.stock_config_use_take_profit_first_part
            use_take_profit_first_part_two = trading_config.stock_config_use_take_profit_first_part_two
            use_bolinger_a_part_to_take_profit = trading_config.stock_config_use_bolinger_a_part_to_take_profit
            use_stoch_rsi_to_take_profit = trading_config.stock_config_use_stoch_rsi_to_take_profit
            use_rsi_decrease_to_take_profit = trading_config.stock_config_use_rsi_decrease_to_take_profit
            value_stoch_rsi_to_take_profit = trading_config.stock_config_value_stoch_rsi_to_take_profit
            percent_stoch_rsi_to_take_profit = trading_config.stock_config_percent_stoch_rsi_to_take_profit
            percent_rsi_decrease_to_take_profit = trading_config.stock_config_percent_rsi_decrease_to_take_profit
            percentage_loss = res_stock_balance.get('stock_balance', {}).get('percentage_loss', 0) if res_stock_balance else 0            
            percent_take_profit_sell_first = trading_config.stock_config_percent_take_profit_sell_first*100
            percent_take_profit_sell_first_two = trading_config.stock_config_percent_take_profit_sell_first_two*100
            percent_take_profit_sell_second = trading_config.stock_config_percent_take_profit_sell_second
            percent_take_profit_sell_second_two = trading_config.stock_config_percent_take_profit_sell_second_two
            use_take_profit_trigger = trading_config.stock_config_use_take_profit_trigger
            take_profit_percent = trading_config.stock_config_take_profit_percent*100
            #Tiến hành kiểm tra cách bán
            is_take_profit = False 
            percent_take_profit = percent_take_profit_sell_second  
            messages_take_profit = 'Không chốt lãi' 
            # Tải dữ liệu
            vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type_sell, 
                following_chart_type=following_chart_type_sell,
            )
            # Tải dữ liệu lần 2
            vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type_sell_second, 
                following_chart_type=following_chart_type_sell_second
            )
            if stock_data_trading is None or stock_data_trading_second is None:
                logger.info('Download data không thành công, bỏ qua!')
                message_download_sell = f'Download data symbol {symbol } to sell không thành công. Bỏ qua lượt trade này!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download_sell)                 
                return
            price_current = stock_data_trading.iloc[-1]['close']    
            upper_bolinger = stock_data_following.iloc[-1]['upper_bolinger']
            latest_stoch_rsi_following  = stock_data_following.iloc[-1]['stoch_rsi']
            current_rsi_following  = stock_data_following.iloc[-1]['rsi']
            previous_rsi_following = stock_data_following.iloc[-2]['rsi']
            take_profit_type = ''
            if  ( (percentage_loss >= take_profit_percent and use_take_profit_trigger) 
                 or (use_take_profit_first_part_two and percentage_loss >= percent_take_profit_sell_first_two) 
                 or (use_take_profit_first_part and percentage_loss >= percent_take_profit_sell_first)
                ):
                # Chốt lãi khi giá hiện tại tăng so với giá vốn 
                logger.info(f'Chốt lãi khi giá hiện tại tăng so với giá vốn {symbol}')
                is_take_profit, percent_take_profit, messages_take_profit = should_sell_take_profit(symbol, trading_config, percentage_loss)
                take_profit_type = (
                    'Bán lần 1 theo phần trăm lời'
                    if use_take_profit_first_part
                    else ('Bán lần 2 theo phần trăm lời' if use_take_profit_first_part_two else 'Bán hết theo phần trăm lời')
                )
            elif use_stoch_rsi_to_take_profit and latest_stoch_rsi_following >= value_stoch_rsi_to_take_profit:
                # Chốt lãi khi stoch_rsi hiện tại >= 
                logger.info(f'Chốt lãi khi stoch_rsi hiện tại >= {symbol}')
                is_take_profit, percent_take_profit = True, percent_stoch_rsi_to_take_profit
                messages_take_profit=f'Bắt đầu chạy chart hành động chốt lãi lần 1 {symbol} vì stoch_rsi(chart theo dõi) hiện tại({latest_stoch_rsi_following}) >= stoch rsi cấu hình({value_stoch_rsi_to_take_profit})'
                take_profit_type = 'Bán một phần khi stoch_rsi >='
            elif use_bolinger_a_part_to_take_profit and price_current >= upper_bolinger:
                # Chốt lãi khi giá hiện tại chạm bolllinger
                logger.info(f'Chốt lãi khi giá hiện tại chạm bolllinger {symbol}')    
                is_take_profit, percent_take_profit, messages_take_profit = should_take_profit_bolinger(symbol, trading_config, price_current, upper_bolinger )
                take_profit_type = 'Bán một phần khi chạm bollinger trên'
            if use_rsi_decrease_to_take_profit and current_rsi_following < previous_rsi_following:
                # Chốt lãi khi giá rsi giảm
                logger.info(f'Chốt lãi khi giá rsi giảm {symbol}')                
                is_take_profit, percent_take_profit = True, percent_rsi_decrease_to_take_profit
                messages_take_profit=f'Bắt đầu chạy chart hành động chốt lãi lần 1 {symbol} vì RSI(chart theo dõi) giảm, RSI D1: {previous_rsi_following} > RSI D0: {current_rsi_following}'
                take_profit_type = 'Bán một phần khi RSI giảm'
            volume_take_profit = int(volume_balance*percent_take_profit)
            volume_take_profit = ((volume_take_profit + 99) // 100) * 100     
            is_trading_take_profit = False
            is_sell, sell_reason = False, ''
            is_sell_following = False  
            if is_take_profit:
                ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
                send_message_telegram(user, MessageTypeEnum.OVERALL, messages_take_profit)
                send_message_telegram(user, MessageTypeEnum.ACT, messages_take_profit)
                start_time = datetime.now()
                end_time = start_time + timedelta(minutes=15)
                status_sell = SignalTelegramEnum.TAKE_PROFIT_FAILED
                while datetime.now() < end_time:
                    # Tải dữ liệu lần 1
                    vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_sell, 
                        following_chart_type=following_chart_type_sell,
                    )
                    # Tải dữ liệu lần 2
                    vnindex_data_trading_second, vnindex_data_following_second, stock_data_trading_second, stock_data_following_second = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_sell_second, 
                        following_chart_type=following_chart_type_sell_second
                    )
                    if stock_data_trading is None or stock_data_trading_second is None:
                        logger.info('Download data không thành công, bỏ qua!')
                        message_download = f'Không tải được dữ liệu mã {symbol}, hủy bán chốt lời lượt chạy này!'
                        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                        send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                        break
                    logger.info('Download data thành công!')
                    is_sell, sell_reason = should_sell_trading(
                        trading_config=trading_config,
                        data_trading_df=stock_data_trading,            
                        config_type='stock_config',
                        data_trading_df_second=stock_data_trading_second
                    )
                    if is_sell:
                        is_trading_take_profit = True            
                        break
                    else:
                        status_sell = SignalTelegramEnum.TAKE_PROFIT_FAILED
                        messages_to_sell = render_message(
                            sell_reason, trading_chart_value=trading_candle_sell, trading_chart_value_second=trading_candle_sell_second, following_chart_type=following_candle_sell, following_chart_type_second=following_candle_sell_second
                        )
                        take_profit_attrs = {
                            "user_account": account,
                            "stock": stock.name,
                            "message": messages_to_sell,
                        }
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **take_profit_attrs) 
                    connection.close()
                    time.sleep(30)
                
                if not is_trading_take_profit:
                    message_timeout_take_profit = f'Đã hết thời gian chờ chốt lời (15 phút) cho {symbol}. Hủy theo dõi chốt lời đợt này.'
                    send_message_telegram(user, MessageTypeEnum.OVERALL, message_timeout_take_profit)
                    send_message_telegram(user, MessageTypeEnum.ACT, message_timeout_take_profit)  
            else:
                is_sell_following, is_sell, sell_reason = should_sell(
                    trading_config=trading_config,
                    following_config=following_config,
                    data_trading_df=stock_data_trading,
                    data_trading_df_second=stock_data_trading_second,
                    data_following_df=stock_data_following,
                    data_following_df_second=stock_data_following_second,
                    config_type='stock_config'
                )


            if is_trading_take_profit:
                status_sell = SignalTelegramEnum.TAKEPROFIT
            elif is_sell:
                status_sell = SignalTelegramEnum.SELL_SUCCESS
            else:
                status_sell = SignalTelegramEnum.SELL_FAILED
            #Tiến hành các bước kế tiếp            
            messages_to_sell = render_message(
                sell_reason, trading_chart_value=trading_candle_sell, following_chart_type=following_candle_sell, trading_chart_value_second=trading_candle_sell_second, following_chart_type_second=following_candle_sell_second)
            price_to_start = (
                stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close'])/2
            price_current = stock_data_trading.iloc[-1]['close']
            sell_attrs = {
                "user_account": account,
                "platform_trading": "Smart One",
                "stock": stock.name,
                "volume": 0,
                "price": price_to_start,
                "message": messages_to_sell
            }
            sell_take_profit = {
                "user_account": account,
                "platform_trading": "Smart One",
                "stock": stock.name,
                "volume": volume_take_profit if use_take_profit_first_part else int(volume_balance),
                "price": price_to_start,                
                "take_profit_type": take_profit_type,
                "message": messages_to_sell
            }
            if is_sell_following:           
               send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)    
            is_send_order_sell = False   

            if status_sell in [SignalTelegramEnum.SELL_SUCCESS, SignalTelegramEnum.TAKEPROFIT]:
                logger.info(f'bắt đầu đặt lệnh sell {symbol} (Đã có lock từ đầu)')
                
                # Vì đã lock từ đầu hàm, nên ở đây ta coi như update success (Logic check cũ đã được xóa)
                timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                last_row = stock_data_trading.iloc[-1]
                open_last_row = last_row['open']
                close_last_row = last_row['close']
                low_last_row = last_row['low']
                high_last_row = last_row['high']
                step_price = trading_config.stock_config_slippage_volume_sell_per_pid
                sleeping_time_sell= trading_config.stock_config_time_update_pid_sell
                sleeping_time_sell = sleeping_time_sell if sleeping_time_sell > 5 else 5
                time_to_sell = trading_config.stock_config_time_to_sell
                time_to_sell = time_to_sell if time_to_sell >= 30 else 30   
                start_price = round_up_to_unit(open_last_row, close_last_row, step_price)  
                number_order = trading_config.stock_config_number_pid_sell_once_time
                time_now = datetime.now(timezone)
                start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                slippage_sell = trading_config.stock_config_slippage_sell
               # Dao động cộng trừ     
                add_price_sell = trading_config.stock_config_add_price_sell
    
                # Get stock balance to set volume
                volume = volume_take_profit if is_take_profit else int(volume_balance)
                sell_order_overrall_attrs = {
                    'user_account': account,
                    'stock': symbol,
                    'volume': int(volume),
                    'start_price': round(start_price, 2),
                    'limit_price': round(start_price + add_price_sell - slippage_sell, 2),
                    "current_price": round(price_current, 2),
                    'step_price': step_price,
                    "slippage_sell": slippage_sell,
                    "add_price_sell": add_price_sell,
                    "sleeping_time_sell": int(sleeping_time_sell), 
                    'number_order': int(number_order),
                    'start_time_order': start_time_order
                }
                sell_messages = []
                sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_OVERRAL,
                                    **sell_order_overrall_attrs })
                
                if volume >= 100:
                # Xử lý bán nhạy cảm 
                if trading_config.stock_config_is_mode_sensitive_sell:
                    sensitive_percentage = trading_config.stock_config_percent_sensitive_sell
                    volume_sell_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                    volume_sell_sensitive = volume_sell_sensitive if volume_sell_sensitive >= 100 else 100
                    price_set_sell = max(start_price, price_current)
                    sell_order_attrs_send = {
                        'stock': symbol,
                        # 'price': round(float(low_last_row + add_price_sell), 2) if round(float(low_last_row + add_price_sell), 2) < ceil_price else round(ceil_price, 2) , 
                        'price': round(price_set_sell, 2), 
                        'volume': int(volume_sell_sensitive)
                    }
                    res_sell = handle_sell_service(user_name, account, request_url, symbol, session, asp_net_session, sell_order_attrs_send['price'],  sell_order_attrs_send['volume'], ref_id)
                    if res_sell:
                        is_send_order_sell = True
                        sell_order_sensitive_attrs = {
                            'stock': res_sell['symbol'],
                            'price': round(res_sell['price'], 2),
                            'volume': res_sell['volume'],
                            'status': res_sell['status'],
                        }
                        sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_DETAIL,
                                            **sell_order_sensitive_attrs })
                        volume -= int(res_sell['volume'])
                        number_order -= 1
                    else:
                        logger.info(f"Error: lệnh bán nhạy cảm handle_sell_service  của {symbol} phản hồi là rỗng") 
                # Chia đều phần còn lại của volume to sell
                if volume >= 100:
                    number_order = min(number_order, volume // 100)
                    for i in range(int(number_order)):
                        divisor = number_order - i
                        if i != int(number_order) - 1:
                            volume_sell = round_to_nearest_hundred(volume / divisor)
                        else:
                            volume_sell = round_to_nearest_hundred(volume / divisor) if volume % 100 != 0 else int(volume)
                        volume -= volume_sell
                        #Gửi các lệnh sell
                        ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
                        price = round(start_price + add_price_sell + i*step_price, 2) if round(start_price + add_price_sell + i*step_price, 2) < ceil_price else round(ceil_price, 2)
                        if volume_sell >= 100:
                            res_sell = handle_sell_service(user_name, account, request_url, symbol, session, asp_net_session, price,  volume_sell, ref_id)
                            if res_sell:
                                is_send_order_sell = True
                                sell_order_details_attrs = {
                                    'stock': res_sell['symbol'],
                                    'price': round(res_sell['price'], 2),
                                    'volume': res_sell['volume'],
                                    'status': res_sell['status'],
                                }                
                                sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_DETAIL,
                                                    **sell_order_details_attrs })
                        else:
                            logger.info(f"Error: lệnh bán lần thứ {i+1} hàm handle_sell_service  của {symbol} có phản hồi là rỗng") 
                # Send telegram tổng hợp khi thực hiện đặt xong các lệnh bán
                if is_send_order_sell:
                    if status_sell == SignalTelegramEnum.TAKEPROFIT: 
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_take_profit) 
                        send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_sell, **sell_take_profit) 
                    else: 
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)
                        send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_sell, **sell_attrs)

                    send_telegram_message_batch(user, MessageTypeEnum.OVERALL, sell_messages)
                    send_telegram_message_batch(user, MessageTypeEnum.ACT, sell_messages) 
                logger.info('kết thúc hàm đặt lệnh sell')
               
            # Xử lý sửa lệnh
            if is_send_order_sell:
                limited_times = time_to_sell // sleeping_time_sell
                limited_price_to_sell = start_price + add_price_sell - slippage_sell
                interval_check = 10  # kiểm tra mỗi 10 giây
                should_break_loop = False  # Flag để thoát khỏi vòng for                
                for i in range(int(limited_times) - 1):
                    if should_break_loop:
                        break
                    start_sleep = time.time()
                    while time.time() - start_sleep < sleeping_time_sell:
                        connection.close()
                        
                        remaining = sleeping_time_sell - (time.time() - start_sleep)
                        sleep_time = min(interval_check, remaining)
                        
                        if sleep_time <= 0:
                            break
                            
                        time.sleep(sleep_time)                        
                        # 🔄 Lấy lại prepared mới mỗi lần lặp để cập nhật cấu hình mới nhất
                        try:
                            configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(
                                user=user, 
                                stock_symbol=symbol
                            )
                            if configuration:
                                refreshed_overview_config = configuration.get("overview_config")                             
                                if refreshed_overview_config:
                                    overview_config = refreshed_overview_config
                        except Exception as e:
                            logger.info(f'Lỗi khi lấy lại cấu hình bán cho {symbol}: {e}')
                            # Tiếp tục dùng config cũ nếu lỗi
                        is_block_sell_stock = overview_config.is_block_sell
                        logger.info(f'check is_block_sell_stock mỗi {interval_check}s {symbol}: {is_block_sell_stock}')
                        if is_block_sell_stock:
                            logger.info(f'{symbol} đã bị chặn bán, hủy lệnh bán {symbol}')
                            cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Đã bị chặn bán', "S")
                            should_break_loop = True
                            break
                        is_time_valid_to_sell  = is_valid_time_to_sell(following_config)
                        if not is_time_valid_to_sell:
                            logger.info(f'{symbol} đã vượt khung giờ bán, hủy lệnh bán {symbol}')
                            cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Đã vượt khung giờ bán', "S")
                            should_break_loop = True
                            break
                    times_update = i + 1
                    message_update = update_sell_order(user_name, account, symbol, request_url, session, asp_net_session, "S", step_price, limited_price_to_sell, times_update)
                    if message_update:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                    else:
                        cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lỗi không sửa được lệnh bán', "S")
                        break  
                else:
                    # Vòng for chạy hết mà không gặp break (tức là số vòng chạy đạt limited_times
                    cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Vượt quá thời gian tối đa đặt lệnh bán', "S")
                    pass
             #Tổng kết các lệnh đã khớp theo symbol để send telegram           
                res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'S')
                if res_matcheds:
                    logger.info(f'danh sách các lệnh bán {symbol} đã khớp: {res_matcheds}')
                    # time_now = datetime.now(timezone)
                    # start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
                    message_sell_matched = []
                    sell_matched_overrall_attrs = {
                        'user_account': account,
                        'stock': symbol,
                        'number_order': len(res_matcheds),
                        } 
                    message_sell_matched.append({
                        'status_signal': SignalTelegramEnum.SELL_MATCHED_OVERRAL,
                        **sell_matched_overrall_attrs
                        })
                    for order in res_matcheds:
                        sell_matched_details_attrs = {
                            'stock': order['symbol'],
                            'price': order['showPrice'],
                            'volume': order['volume'],
                            'status': order['status']
                            }
                        message_sell_matched.append({
                            'status_signal': SignalTelegramEnum.SELL_MATCHED_DETAIL,
                            **sell_matched_details_attrs
                            })
                    if message_sell_matched:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_sell_matched)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_sell_matched)

             #Trả lại trạng thái
                if status_sell == SignalTelegramEnum.TAKEPROFIT and take_profit_type != 'Bán hết theo phần trăm lời': 
                    logger.info('Tiến hành đóng chốt lãi một phần cho 4 loại ....') 
                    ConfigurationServices.update_all_take_profit_flags_false(user, stock_id, use_take_profit_first_part)

        logger.info(f'Kết thúc process_trading: {symbol}')
    except Exception as e:
        logger.info(f"Error in {current_thread_name}: {str(e)}")
    finally:
        if stock_id:
             try:
                is_manual_final = False
                config_final = ConfigurationServices.get_user_configuration_by_stock_symbol(user, symbol)
                if config_final:
                    overview_final = config_final.get("overview_config")
                    if overview_final and (overview_final.is_buy_hand or overview_final.is_sell_hand):
                         is_manual_final = True
                
                if not is_manual_final:
                     ConfigurationServices.update_is_trading_configuration(user, stock_id, False)
                     logger.info(f"Đã reset is_trading cho {symbol} trong finally block")
                else:
                     logger.info(f"Giữ is_trading=True cho {symbol} trong finally block vì đang Mua/Bán Tay")
             except Exception as e_final:
                logger.error(f"Lỗi khi reset is_trading trong finally cho {symbol}: {e_final}")

        # Đóng connection của thread hiện tại
        connection.close()


def  trading_configurations(user: User, configurations: object, vps_account: Account, percent_buy_trade: float) -> None:
    logger.info('Job trading_configurations is running...')

    # Lấy dữ liệu cần thiết
    vnindex_stock = StockService.get_stock_by_symbol('VNINDEX')
    limit_number_stocks = vps_account.limit_number_stocks

    # Chuẩn bị dữ liệu cấu hình cho từng cổ phiếu
    prepared_configs = []
    for configuration in configurations:
        trading_config = configuration.get("trading_config")
        following_config = configuration.get("following_config")
        overview_config = configuration.get("overview_config")
        stock = configuration.get("stock")

        # Lấy giá trị candle từ trading_config và following_config, dùng giá trị mặc định nếu chưa có
        # candle và candle_sell: lấy từ trường tương ứng của Candle object
        trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
        trading_candle_sell = getattr(getattr(trading_config, "candle_sell", None), "candle_sell", "M5")
        following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
        following_candle_sell = getattr(getattr(following_config, "candle_sell", None), "candle_sell", "D1")
        
        # candle_second và candle_sell_second: lấy từ trường candle/candle_sell của Candle object (giống logic trong services.py)
        # Vì get_candle_second() tìm Candle object có candle="D1", nên cần lấy từ trường candle, không phải candle_second
        trading_candle_second = getattr(getattr(trading_config, "candle_second", None), "candle", "M5")
        trading_candle_sell_second = getattr(getattr(trading_config, "candle_sell_second", None), "candle_sell", "M5")
        following_candle_second = getattr(getattr(following_config, "candle_second", None), "candle", "D1")
        following_candle_sell_second = getattr(getattr(following_config, "candle_sell_second", None), "candle_sell", "D1")

        # Xác định kiểu biểu đồ dựa trên enum (có thể điều chỉnh theo logic cụ thể)
        trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
        trading_chart_type_second = getattr(CandleEnum, trading_candle_second, CandleEnum.M5)
        trading_chart_type_sell = getattr(CandleEnum, trading_candle_sell, CandleEnum.M5)
        trading_chart_type_sell_second = getattr(CandleEnum, trading_candle_sell_second, CandleEnum.M5)
        following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
        following_chart_type_second = getattr(CandleEnum, following_candle_second, CandleEnum.D1)
        following_chart_type_sell = getattr(CandleEnum, following_candle_sell, CandleEnum.D1)
        following_chart_type_sell_second = getattr(CandleEnum, following_candle_sell_second, CandleEnum.D1)
        prepared_configs.append({
            "trading_candle": trading_candle,
            "trading_candle_second": trading_candle_second,
            "trading_candle_sell": trading_candle_sell,
            "trading_candle_sell_second": trading_candle_sell_second,
            "following_candle": following_candle,
            "following_candle_second": following_candle_second,
            "following_candle_sell": following_candle_sell,
            "following_candle_sell_second": following_candle_sell_second,
            "trading_chart_type": trading_chart_type,
            "trading_chart_type_second": trading_chart_type_second,
            "trading_chart_type_sell": trading_chart_type_sell,
            "trading_chart_type_sell_second": trading_chart_type_sell_second,
            "following_chart_type": following_chart_type,
            "following_chart_type_second": following_chart_type_second,
            "following_chart_type_sell": following_chart_type_sell,
            "following_chart_type_sell_second": following_chart_type_sell_second,
            "stock": stock,
            "trading_config": trading_config,
            "following_config": following_config,
            "overview_config": overview_config,
        })

    # Hàm worker cho mỗi cấu hình
    def worker(prepared):
        close_old_connections()
        try:
            process_trading(
                prepared, 
                user, 
                vnindex_stock, 
                vps_account, 
                percent_buy_trade,
            )
        finally:
            # Đóng connections của thread hiện tại
            connection.close()

    # Khôi phục 100 worker để đảm bảo chạy đủ mã của user.
    # Độ ổn định dựa vào logic try/except đóng kết nối ở trên.
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for config in prepared_configs:
            try:
                futures.append(executor.submit(worker, config))
                time.sleep(0.2)  # Thêm độ trễ giữa các luồng
            except RuntimeError as e:
                logger.info(f"Cannot submit new task: {e}")
                break  # Dừng nếu executor đã shutdown

        # Chờ các task hoàn thành và xử lý ngoại lệ (nếu có)
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.info(f"Error in thread: {e}")

    
def trading(user: User, vps_account: Account, symbol: str) -> None:
    logger.info('Job trading is running...')
    
    # Cache cấu hình người dùng và thông tin cổ phiếu VNINDEX
    user_configurations = ConfigurationServices.get_and_sort_user_configuration_by_level(user=user)
    account_name = vps_account.name
    account_num = vps_account.account_num
    session_id = vps_account.vps_session_id
    limit_number_stocks = vps_account.limit_number_stocks
    #Lấy ds symbol đang trading
    request_url = api.TRADING_URL
    configurations_is_trading = [
        config for config in user_configurations
        if (trading_config := config.get("trading_config")) and trading_config.is_trading is True
    ]
    list_symbol_is_trading  = [
        config["stock"].name
        for config in configurations_is_trading
    ]
    logger.info(f'List symbol_is_trading của user {user.username}: {list_symbol_is_trading}  ')
    message_is_trading = f'Danh sách các mã đang hoạt động: {list_symbol_is_trading}  '
    send_message_telegram(user, MessageTypeEnum.OVERALL, message_is_trading) 
    configurations_handle_trading = [
        config for config in user_configurations
        if (trading_config := config.get("trading_config")) and trading_config.is_trading is False
    ]
    list_symbol_not_trading  = [
        config["stock"].name
        for config in configurations_handle_trading
    ]
    # logger.info('List symbol_not_trading: ', list_symbol_not_trading )

    # Get stock balance 
    res_stock_balance = handle_stock_balance_service(account_name, account_num, '', request_url, session_id, '','' )    
    number_stock_existing = res_stock_balance.get('number_stock_existing', 0) if res_stock_balance else 0
    percent_buy_trade = res_stock_balance.get('percent_buy_trade', 0) if res_stock_balance else 0
    symbols_existing = res_stock_balance.get('symbols_existing', []) if res_stock_balance else []
   
    if number_stock_existing >= limit_number_stocks:
        configurations_handle_trading = [
            config for config in configurations_handle_trading
            if (stock := config.get("stock")) and stock.name in symbols_existing ]
    list_symbols_process_trading  = [
        config["stock"].name
        for config in configurations_handle_trading
    ]
    logger.info(f'List list_symbols_process_trading của user {user.username} : {list_symbols_process_trading} ')
    message_process_trading = f'Danh sách các mã đang theo dõi: {list_symbols_process_trading}  '
    send_message_telegram(user, MessageTypeEnum.OVERALL, message_process_trading) 
    trading_configurations(user, configurations_handle_trading, vps_account, percent_buy_trade)


def trading_request(user: User, vps_account: Account, stock_id: str, symbol: str, request_buy: bool, request_sell: bool, volume_sell: str, is_use_chart_action: bool) -> bool:
    logger.info('Job request trading is running...')

    vnindex_stock = StockService.get_stock_by_symbol('VNINDEX')
    limit_number_stocks = vps_account.limit_number_stocks
    prepared_configs = []

    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
    trading_config = configuration.get("trading_config", {})
    following_config = configuration.get("following_config", {})
    overview_config = configuration.get("overview_config", {})

    stock = configuration.get("stock")

    # candle và candle_sell: lấy từ trường tương ứng của Candle object
    trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
    trading_candle_sell = getattr(getattr(trading_config, "candle_sell", None), "candle_sell", "M5")
    following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
    following_candle_sell = getattr(getattr(following_config, "candle_sell", None), "candle_sell", "D1")
    
    # candle_second và candle_sell_second: lấy từ trường candle/candle_sell của Candle object (giống logic trong services.py)
    trading_candle_second = getattr(getattr(trading_config, "candle_second", None), "candle", "M5")
    trading_candle_sell_second = getattr(getattr(trading_config, "candle_sell_second", None), "candle_sell", "M5")
    following_candle_second = getattr(getattr(following_config, "candle_second", None), "candle", "D1")
    following_candle_sell_second = getattr(getattr(following_config, "candle_sell_second", None), "candle_sell", "D1")

    trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
    trading_chart_type_second = getattr(CandleEnum, trading_candle_second, CandleEnum.M5)
    trading_chart_type_sell = getattr(CandleEnum, trading_candle_sell, CandleEnum.M5)
    trading_chart_type_sell_second = getattr(CandleEnum, trading_candle_sell_second, CandleEnum.M5)
    following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
    following_chart_type_second = getattr(CandleEnum, following_candle_second, CandleEnum.D1)
    following_chart_type_sell = getattr(CandleEnum, following_candle_sell, CandleEnum.D1)
    following_chart_type_sell_second = getattr(CandleEnum, following_candle_sell_second, CandleEnum.D1)

    prepared_configs.append({
        "trading_candle": trading_candle,
        "trading_candle_second": trading_candle_second,
        "trading_candle_sell": trading_candle_sell,
        "trading_candle_sell_second": trading_candle_sell_second,
        "following_candle": following_candle,
        "following_candle_second": following_candle_second,
        "following_candle_sell": following_candle_sell,
        "following_candle_sell_second": following_candle_sell_second,
        "trading_chart_type": trading_chart_type,
        "trading_chart_type_second": trading_chart_type_second,
        "trading_chart_type_sell": trading_chart_type_sell,
        "trading_chart_type_sell_second": trading_chart_type_sell_second,
        "following_chart_type": following_chart_type,
        "following_chart_type_second": following_chart_type_second,
        "following_chart_type_sell": following_chart_type_sell,
        "following_chart_type_sell_second": following_chart_type_sell_second,
        "stock": stock,
        "trading_config": trading_config,
        "following_config": following_config,
        "overview_config": overview_config,
    })

    def run_process_buy():
        close_old_connections()
        process_buy_request(
            prepared_configs[0], user, vnindex_stock, vps_account, stock_id, limit_number_stocks, request_buy, request_sell, is_use_chart_action
        )

    def run_process_sell():
        close_old_connections()
        process_sell_request(
            prepared_configs[0], user, vnindex_stock, vps_account, stock_id, limit_number_stocks, request_buy, request_sell, volume_sell, is_use_chart_action
        )

    if prepared_configs:
        logger.info(f'check length prepared_configs: {len(prepared_configs)}')
        if request_buy:
            threading.Thread(target=run_process_buy).start()
            return True
        elif request_sell:
            threading.Thread(target=run_process_sell).start()
            return True
    else:
        logger.info("Không có dữ liệu trong prepared_configs, bỏ qua process_trade_request.")
        return False

