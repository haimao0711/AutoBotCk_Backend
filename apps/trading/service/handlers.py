from django.utils import timezone
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
from apps.trading.service.helper import (render_message, round_to_nearest_hundred, should_sell_take_profit, should_take_profit_bolinger, 
                                         send_telegram_message, send_telegram_message_batch, should_buy, should_buy_following, should_buy_trading, should_sell, should_sell_trading)
from apps.trading.service.utils import round_up_to_unit, revert_status_request_trade
from apps.telegram.sender import send_message, send_message_telegram

# from apps.balance.services import BalanceService

from common.signal.enums import SignalTelegramEnum
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
    print(f'Bắt đầu chạy hàm cancel all order ')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', side)    
    if res_not_matcheds:
        print(f'Da co danh sach chua khop to cancel all order: ', res_not_matcheds)

        for order in res_not_matcheds: 
            res_cancel = handle_cancel_order_service(user_name, request_url, session, '', order['orderNo'], ref_id)
            if res_cancel:
                print(f"Da huy lenh {order['side']} mã {order['symbol']}: {res_cancel}")
            else:
                print(f'Chua huy duoc lenh sell {symbol}')
        message_cancel = '📢📢📢** Khởi động lại Bot, đã hủy tất cả các lệnh đang đặt hiện tại** 📢📢📢'
        send_message_telegram(user, MessageTypeEnum.OVERALL, message_cancel)
        send_message_telegram(user, MessageTypeEnum.ACT, message_cancel)  
    else:
        print(f'Chua lay duoc danh sach chua khop to cancel all orrder')



def update_buy_order(user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str, step_price: float, limited_price: float, times_update: int):
    print(f'Bắt đầu chạy hàm update lệnh mua {symbol} ' )    
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time_update = datetime.now(tz)
    start_time = time.time()  # Lấy thời gian bắt đầu
    print(f'Nhắc lại giới hạn update lệnh mua {symbol}: ', limited_price )
    max_retry = 5
    retry_count = 0
    res_not_matcheds = None

    # Lặp lại tối đa max_retry lần hoặc cho đến khi lấy được danh sách chưa khớp
    while not res_not_matcheds and retry_count < max_retry:
        res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', 'B')

        if not res_not_matcheds:
            retry_count += 1
            print(f"Lần thử {retry_count}/{max_retry}: Chưa có danh sách chưa khớp cho symbol {symbol}. Thử lại sau {5} giây...")
            time.sleep(5)

    message_buy_update = []

    if res_not_matcheds:
        print(f"Đã có danh sách chưa khớp để update buy stock {symbol}: {res_not_matcheds}")
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
                    handle_update_order_service(user_name, account, request_url, symbol, session, '', order_num, old_price, update_price, update_volume, ref_id, 'B')
                    buy_update_details_attrs = {
                        'stock': order['symbol'],
                        'old_price': old_price,
                        'update_price': update_price,
                        'volume': order['volume'],
                        'status': order['status']
                    }
                    print('check data update buy: ', buy_update_details_attrs)
                    message_buy_update.append({
                            'status_signal': SignalTelegramEnum.BUY_UPDATE_DETAIL,
                            **buy_update_details_attrs
                    })
                
            # Nếu update_price vượt quá limited_price thì handle cancel order
                else:
                    print(f'Huy lenh vi gia update: {update_price} da toi limited: {limited_price}')
                    res_cancel_order = handle_cancel_order_service(user_name, request_url, session, '', order_num, ref_id)
                    if res_cancel_order:
                        print(f'Da huy lenh mua {symbol}: ', res_cancel_order)
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
                        print(f'Chua huy duoc lenh mua one order {symbol}')
            except Exception as e:
                print(f"[ERROR] Lỗi khi xử lý order {order_num}: {e}")
    else:
        print(f"Thử {max_retry} lần nhưng vẫn chưa có danh sách chưa khớp để update buy stock {symbol}. Ngưng update lệnh")

    return message_buy_update 

def cancel_buy_order(user: User,user_name: str, account: str, symbol: str, request_url: str, session: str, reason: str, side: str):
    print(f'Bắt đầu chạy hàm cancel lệnh mua all oders {symbol} ' )
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    # start_time_cancel = datetime.now(timezone)
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time_cancel = datetime.now(tz)
    message_buy_cancel = []
    res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', 'B')    
    if res_not_matcheds:
        print(f'Da co danh sach chua khop to cancel buy stock {symbol}: ', res_not_matcheds)
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
            res_cancel = handle_cancel_order_service(user_name, request_url, session, '', order['orderNo'], ref_id)
            if res_cancel:
                print(f'Da huy lenh mua {symbol}: ', res_cancel)
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
                print(f'Chua huy duoc lenh mua {symbol}')

        if message_buy_cancel:
            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_buy_cancel)
            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_buy_cancel)
    else:
        print(f'Chua lay duoc danh sach chua khop to cancel buy {symbol}')  
    print(f'Kết thúc chạy hàm cancel lệnh mua {symbol} ' )

def update_sell_order(user_name: str, account: str, symbol: str, request_url: str, session: str, asp_net_session: str, side: str, step_price: float, limited_price: float, times_update: int):
    print(f'Bắt đầu chạy hàm update lệnh bán {symbol} ' )      
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    time_now  = datetime.now(tz)
    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")    
    
    message_sell_update = []
    print(f'Nhắc lại giới hạn update lệnh bán {symbol}: ', limited_price )   
    res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', 'S')
    if res_not_matcheds:
        print(f'da co danh sach chưa khơp to update stock {symbol}: ', res_not_matcheds ) 
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
            print('check order_num sell: ', order_num)
        # Nếu update_price chưa bé hơn limited_price thì handle update order
            if update_price > limited_price:
                handle_update_order_service(user_name, account, request_url, symbol, session, '', order_num, old_price, update_price, update_volume, ref_id, 'S')
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
                print(f'Huy lenh vi gia update: {update_price} da toi limited: {limited_price}')
                res_cancel_order = handle_cancel_order_service(user_name, request_url, session, '', order_num, ref_id)
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
                    print(f'Chua huy duoc lenh mua one order {symbol}') 
    else: 
        print(f'chưa lấy được res danh sach chưa khơp to update sell {symbol} ' )

    return message_sell_update  

def cancel_sell_order(user: User, user_name: str, account: str, symbol: str, request_url: str, session: str, reason: str, side: str):
    print(f'Bắt đầu chạy hàm cancel lệnh sell {symbol}')
    ref_id = f"{user_name}.I.test.{int(time.time()*1000)}"
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    time_now  = datetime.now(tz)
    start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y") 
    message_cancel = []
    res_not_matcheds = handle_orders_not_matched(user_name, account, symbol, request_url, session, '', 'S')    
    if res_not_matcheds:
        print(f'Da co danh sach chua khop to cancel sell stock {symbol}: ', res_not_matcheds)
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
            res_cancel = handle_cancel_order_service(user_name, request_url, session, '', order['orderNo'], ref_id)
            if res_cancel:
                print(f'Da huy lenh ban {symbol}: ', res_cancel)
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
                print(f'Chua huy duoc lenh sell {symbol}')
                pass
        # Send telegram   
        if message_cancel:
            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_cancel)
            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_cancel)
        else:
            print(f'Chua lay duoc danh sach chua khop to cancel sell {symbol}')  

def process_buy_request(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, stock_id: str, limit_number_stocks: int, request_buy: bool, request_sell: bool):
    # Các giá trị mặc định
    print('bat dau chay ham process_buy_request!! ')
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    user_name = vps_account.name
    account = vps_account.account_num
    session = vps_account.vps_session_id
    request_url = api.TRADING_URL
    ref_id = f"{user_name}.I.test.{int(time.time() * 1000)}"    
    
    # Lấy dữ liệu đã chuẩn bị  
    trading_candle = prepared["trading_candle"]
    following_candle = prepared["following_candle"]
    trading_chart_type = prepared["trading_chart_type"]
    following_chart_type = prepared["following_chart_type"]
    trading_config = prepared["trading_config"]       
    overview_config = prepared["overview_config"]
    stock = prepared["stock"]
    symbol = stock.name        
    asp_net_session = ''
    max_stock_existing = limit_number_stocks

    print('Cổ phiếu đang request buy:', {symbol})     
   
    slippage_buy = trading_config.stock_config_slippage_buy
    add_price_buy = trading_config.stock_config_add_price_buy
    level = overview_config.level

    #HANDLE BUY
    # Xác định thời gian bắt đầu và thời gian kết thúc (sau 1 tiếng)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    status_buy = SignalTelegramEnum.BUY_REQUEST_FAILED
    last_buy_check_time = None  # Dùng để giới hạn việc kiểm tra mua mỗi 60 giây
    message_stop_buy = 'Hết thời gian của lệnh mua tay'
    ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
    while datetime.now() < end_time:
        # Kiểm tra is_buy_hand mỗi 5 giây        
        configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
        overview_config = configuration.get("overview_config", {})
        is_buy_hand = overview_config.is_buy_hand
        print(f'check is_buy_hand overview_config {symbol} : ', is_buy_hand)

        if not is_buy_hand:
            print(f'Dừng mua tay cổ phiếu {symbol} : ', is_buy_hand)
            message_stop_buy = 'Yêu cầu ngừng mua tay'
            break  # Thoát khỏi vòng while và tiếp tục đoạn code phía sau

        # Kiểm tra điều kiện mua chỉ mỗi 60 giây một lần
        now = datetime.now()
        if last_buy_check_time is None or (now - last_buy_check_time).total_seconds() >= 60:
            last_buy_check_time = now

            # === XỬ LÝ MUA ===
            _, _, stock_data_trading, _ = download_data(
                stock=stock,
                vnindex_stock=vnindex_stock,
                trading_chart_type=trading_chart_type,
                following_chart_type=following_chart_type
            )

            if stock_data_trading is None:
                print('Download data không thành công, bỏ qua!')
                message_download = f'Không tải được dữ liệu mã {symbol}, hủy yêu cầu mua tay. Vui lòng thử lại sau ít phút'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                revert_status_request_trade(user, stock_id)
                return

            price_to_start = (
                stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close']) / 2

            is_buy, buy_reason = should_buy_trading(
                trading_config=trading_config,
                data_trading_df=stock_data_trading,
                config_type='stock_config'
            )
            logger.info(f'Check is_buy ham request buy {symbol}: {is_buy}')
            logger.info(f'Check buy_reason {symbol}: {buy_reason}')

            if is_buy:
                status_buy = SignalTelegramEnum.BUY_REQUEST_SUCCESS

            messages_to_buy = render_message(
                buy_reason, trading_chart_value=trading_candle, following_chart_type=following_candle
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
                print('Dừng vòng lặp do điều kiện mua thoả mãn.')
                break

        # Chờ 5 giây trước khi kiểm tra lại is_buy_hand
        time.sleep(5)

    if status_buy == SignalTelegramEnum.BUY_REQUEST_FAILED:
        logger.info('Dừng vòng lặp do vượt thời gian hoặc Yêu cầu ngừng mua tay .')        
        revert_status_request_trade(user, stock_id)
        time_now = datetime.now(timezone)
        start_time_order = time_now.strftime("%H:%M:%S ngày %d-%m-%Y")
        buy_attrs = {
            "user_account": account,
            "platform_trading": "Smart One",
            "stock": stock.name,
            "level": level,
            "price": price_to_start,
            "message": message_stop_buy,
            "start_time_order": start_time_order,
        }
        try:
            send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
        except Exception as e:
            print(f"❌ Lỗi khi gửi tin nhắn: {e}") 

    is_send_order_buy = False   
    if status_buy == SignalTelegramEnum.BUY_REQUEST_SUCCESS:
        print(f'bắt đầu hàm đặt lệnh mua tay {symbol}')
    #Hủy tất cả các lệnh nếu còn đặt
        cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Các lệnh mua cũ còn tồn', "B")

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
            volume_by_balance =  int(volume_to_buy - stock_balance)
            volume = int(round(volume_to_buy * percent_first_buy / 100) * 100) if volume_by_balance > int(volume_to_buy*percent_first_buy) else volume_by_balance

            buy_order_overrall_attrs = {
                'user_account': account,
                'stock': symbol,
                'volume': volume,
                'level': level,
                'start_price': round(start_price, 2),
                "current_price": round(price_current, 2),
                'limit_price': round(start_price - add_price_buy + slippage_buy, 2),
                'step_price': step_price,
                "slippage_buy": slippage_buy,
                "add_price_buy": add_price_buy,
                "sleeping_time_buy": sleeping_time_buy,                     
                'number_order': int(number_order),
                'start_time_order': start_time_order
            }

            buy_messages = []
            buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_OVERRAL,
                            **buy_order_overrall_attrs })  
                    
    # Xử lý mua nhạy cảm 
            if volume >=100 and trading_config.stock_config_is_mode_sensitive_buy:
                sensitive_percentage = trading_config.stock_config_percent_sensitive_buy
                volume_buy_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                buy_order_attrs_send = {
                    'stock': symbol,
                    'price': round(float(high_last_row - add_price_buy), 2), # Giá mua tạm thời giảm so với yêu cầu thuật toán, cần sửa lại
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
                    logger.info(f"Error: lệnh mua nhạy cảm handle_buy_service  của {symbol} có phản hồi là rỗng")
            else:
                logger.info(f'Mã {symbol} đạt khối lượng tối đa') 
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
                        print(f"Error: lệnh mua lần thứ {i+1} hàm handle_buy_service  của {symbol} có phản hồi là rỗng") 
                    volume -= volume_buy
            else:
                print(f'Mã {symbol} đạt khối lượng tối đa') 
    # Send telegram tổng hợp khi thực hiện đặt xong các lệnh bán
        if is_send_order_buy:
            send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
            send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_buy, **buy_attrs)             
            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, buy_messages)
            send_telegram_message_batch(user, MessageTypeEnum.ACT, buy_messages)
        
        print(f'kết thúc hàm đặt lệnh request buy {symbol}')        
    
    # Update buy order
    if is_send_order_buy: 
        time.sleep(sleeping_time_buy)
        limited_times = time_to_buy // sleeping_time_buy
        limited_price_to_buy = start_price - add_price_buy + slippage_buy
        for i in range(int(limited_times) - 1):    
            status_buy = SignalTelegramEnum.BUY_SUCCESS
            times_update = i + 1
            message_update = update_buy_order(user_name, account, symbol, request_url, session, asp_net_session, "B", 
                                              step_price, limited_price_to_buy, times_update)
            if  message_update:
                send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                time.sleep(sleeping_time_buy)
            else:
                print(f"Sửa lệnh thất bại ở lần thứ {times_update}, sẽ huỷ lệnh.")                
                cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Sửa lệnh mua không thành công', "B")
                revert_status_request_trade(user, stock_id)
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
                print('Không lấy được danh sách các lệnh đã khớp symbol: ', symbol)
        except Exception as e:
            print(f"Lỗi khi xử lý matched orders: {e}")
            message = f'Không lấy được thông tin các lệnh mua tay đã khớp mã {symbol}'
            send_message_telegram(user, MessageTypeEnum.OVERALL, message)
            send_message_telegram(user, MessageTypeEnum.ACT, message)
    #Hủy tất cả các lệnh nếu còn đặt
        cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Hết thời gian mua', "B")
    time.sleep(5)
    revert_status_request_trade(user, stock_id)

def process_sell_request(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, stock_id: str, limit_number_stocks: int, request_buy: bool, request_sell: bool, volume_sell: str):
    # Các giá trị mặc định
    print('bat dau chay ham process_sell_request!! ')
    print('check volume_sell: ', volume_sell)
    user_name = vps_account.name
    account = vps_account.account_num
    session = vps_account.vps_session_id
    request_url = api.TRADING_URL
    ref_id = f"{user_name}.I.test.{int(time.time() * 1000)}"
    
    
    # Lấy dữ liệu đã chuẩn bị  
    trading_candle_sell = prepared["trading_candle_sell"]
    following_candle_sell = prepared["following_candle_sell"]
    trading_chart_type_sell = prepared["trading_chart_type_sell"]
    following_chart_type_sell = prepared["following_chart_type_sell"]
    trading_config = prepared["trading_config"]
    following_config = prepared["following_config"]        
    overview_config = prepared["overview_config"]
    stock = prepared["stock"]
    symbol = stock.name        
    asp_net_session = ''

    print('Cổ phiếu đang request sell:', {symbol})     


    slippage_sell = trading_config.stock_config_slippage_sell
    add_price_sell = trading_config.stock_config_add_price_sell

    #HANDLE SELL
    ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
    # Xác định thời gian bắt đầu và thời gian kết thúc (sau 1 tiếng)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    status_sell = SignalTelegramEnum.SELL_REQUEST_FAILED
    last_buy_check_time = None
    message_stop_sell = 'Hết thời gian của lệnh bán tay'
    while datetime.now() < end_time:
        # Kiểm tra is_sell_hand mỗi 5 giây
        configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
        overview_config = configuration.get("overview_config", {})
        is_sell_hand = overview_config.is_sell_hand
        print(f'check is_buy_hand overview_config {symbol} : ', is_sell_hand)

        if not is_sell_hand:
            print(f'Dừng mua tay cổ phiếu {symbol} : ', is_sell_hand)
            message_stop_sell = 'Yêu cầu dừng bán tay'
            break  # Thoát khỏi vòng while và tiếp tục đoạn code phía sau
        
        # Kiểm tra điều kiện mua chỉ mỗi 60 giây một lần
        now = datetime.now()
        if last_buy_check_time is None or (now - last_buy_check_time).total_seconds() >= 60:
            last_buy_check_time = now

            # === XỬ LÝ MUA ===
            # Tải dữ liệu
            vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type_sell, 
                following_chart_type=following_chart_type_sell,
            )
            if stock_data_trading is None:
                print('Download data không thành công, bỏ qua!')
                message_download = f'Không tải được dữ liệu mã {symbol}, hủy yêu cầu bán tay. Vui lòng thử lại sau ít phút!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                revert_status_request_trade(user, stock_id)
                return
            print('Download data thành công!')
            price_to_start = (
                stock_data_trading.iloc[-1]['open'] + stock_data_trading.iloc[-1]['close'])/2
            print('Check price_to_start: ', price_to_start)
            is_sell, sell_reason = should_sell_trading(
                trading_config=trading_config,
                data_trading_df=stock_data_trading,            
                config_type='stock_config'
            )
            if is_sell:
                status_sell = SignalTelegramEnum.SELL_REQUEST_SUCCESS
            messages_to_sell = render_message(
                sell_reason, trading_chart_value=trading_candle_sell, following_chart_type=following_candle_sell
            )

            sell_attrs = {
                "user_account": account,
                "platform_trading": "Smart One",
                "stock": stock.name,
                "volume": 0,
                "price": price_to_start,
                "message": messages_to_sell,
            }
            send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)    
            
            if status_sell == SignalTelegramEnum.SELL_REQUEST_SUCCESS:              
                print('Dừng vòng lặp do  điều kiện bán thỏa mãn.')
                break 

        time.sleep(5) 

    if status_sell == SignalTelegramEnum.SELL_REQUEST_FAILED:
        print('Dừng vòng lặp do vượt thời gian hoặc yêu cầu ngừng.')
        revert_status_request_trade(user, stock_id)
        sell_attrs = {
            "user_account": account,
            "platform_trading": "Smart One",
            "stock": stock.name,
            "volume": 0,
            "price": price_to_start,
            "message": message_stop_sell,
        }
        try:
            send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)
        except Exception as e:
            print(f"❌ Lỗi khi gửi tin nhắn: {e}") 
    is_send_order_sell = False   
    if status_sell == SignalTelegramEnum.SELL_REQUEST_SUCCESS:
        print(f'bắt đầu hàm đặt lệnh sell {symbol}')
     #Hủy tất cả các lệnh nếu còn đặt
        cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lệnh bán cũ còn tồn', "S")

        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        last_row = stock_data_trading.iloc[-1]
        open_last_row = last_row['open']
        close_last_row = last_row['close']
        low_last_row = last_row['low']
        high_last_row = last_row['high']
        step_price = trading_config.stock_config_slippage_volume_sell_per_pid
        # print(f'check step_price stock {symbol}: ', step_price)
        sleeping_time_sell= trading_config.stock_config_time_update_pid_sell
        
        sleeping_time_sell = sleeping_time_sell if sleeping_time_sell > 5 else 5
        time_to_sell = trading_config.stock_config_time_to_sell
        time_to_sell = time_to_sell if time_to_sell >= 30 else 30
        start_price = round_up_to_unit(open_last_row, close_last_row, step_price)       
        price_current = stock_data_trading.iloc[-1]['close']
        number_order = trading_config.stock_config_number_pid_sell_once_time 
        start_time_order = datetime.now(timezone)
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
            'volume': volume,
            'start_price': round(start_price, 2),
            "current_price": round(price_current, 2),
            'step_price': step_price,
            "slippage_sell": slippage_sell,
            "add_price_sell": add_price_sell,
            "sleeping_time_sell": sleeping_time_sell,
            'limit_price': round(start_price + add_price_sell - slippage_sell, 2),  
            'number_order': int(number_order),
            'start_time_order': start_time_order
        }
        sell_messages = []
        sell_messages.append({'status_signal': SignalTelegramEnum.SELL_ORDER_OVERRAL,
                            **sell_order_overrall_attrs })
        
        if volume >= 100:
        # Xử lý mua nhạy cảm 
            if trading_config.stock_config_is_mode_sensitive_sell:
                sensitive_percentage = trading_config.stock_config_percent_sensitive_sell
                volume_sell_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                volume_sell_sensitive = volume_sell_sensitive if volume_sell_sensitive >= 100 else 100
                sell_order_attrs_send = {
                    'stock': symbol,
                    'price': round(float(low_last_row + add_price_sell), 2) if round(float(low_last_row + add_price_sell), 2) < ceil_price else round(ceil_price, 2) , 
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
                    print(f"Error: lệnh bán nhạy cảm handle_sell_service  của {symbol} phản hồi là rỗng") 
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
                        print(f"Error: lệnh bán lần thứ {i+1} hàm handle_sell_service  của {symbol} có phản hồi là rỗng") 
        # Send telegram tổng hợp khi thực hiện đặt xong các lệnh bán
            if is_send_order_sell:
                send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **sell_attrs)
                send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_sell, **sell_attrs)
                send_telegram_message_batch(user, MessageTypeEnum.OVERALL, sell_messages)
                send_telegram_message_batch(user, MessageTypeEnum.ACT, sell_messages) 
        print('kết thúc hàm đặt lệnh sell')     
    
    if is_send_order_sell:
        time.sleep(sleeping_time_sell)
        limited_times = time_to_sell // sleeping_time_sell
        limited_price_to_sell = start_price + add_price_sell - slippage_sell
        print(f'check limit_price_to_buy {symbol}: ', limited_price_to_sell)
        
        for i in range(int(limited_times) - 1):
            
            status_sell = SignalTelegramEnum.SELL_SUCCESS
            times_update = i + 1
            message_update = update_sell_order(user_name, account, symbol, request_url, session, asp_net_session, "S", step_price, limited_price_to_sell, times_update)
            if message_update:
                send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
            else:
                cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lỗi không sửa được lệnh bán tay', "S")
                revert_status_request_trade(user, stock_id)
                break           
            time.sleep(sleeping_time_sell) 

    #Tổng kết các lệnh đã khớp theo symbol để send telegram 
        try:          
            res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'S')
            if res_matcheds:
                print(f'danh sách các lệnh bán {symbol} đã khớp: ', res_matcheds )
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
            print(f"Lỗi khi xử lý matched orders: {e}")
            message = f'Không lấy được thông tin các lệnh bán tay đã khớp mã {symbol}'
            send_message_telegram(user, MessageTypeEnum.OVERALL, message)
            send_message_telegram(user, MessageTypeEnum.ACT, message)
    #Hủy tất cả các lệnh nếu còn đặt
        cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Hết thời gian đặt lệnh bán tay', "S")
    time.sleep(10) 
    revert_status_request_trade(user, stock_id)

def process_trading(prepared: dict, user: User, vnindex_stock: any, vps_account: Account, percent_buy_trade: float):
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
        trading_candle_sell = prepared["trading_candle_sell"]
        following_candle = prepared["following_candle"]
        following_candle_sell = prepared["following_candle_sell"]
        trading_chart_type = prepared["trading_chart_type"]
        trading_chart_type_sell = prepared["trading_chart_type_sell"]
        following_chart_type = prepared["following_chart_type"]
        following_chart_type_sell = prepared["following_chart_type_sell"]
        trading_config = prepared["trading_config"]
        following_config = prepared["following_config"]        
        overview_config = prepared["overview_config"]
        stock = prepared["stock"]
        symbol = stock.name        
        asp_net_session = ''
        percent_first_buy = trading_config.stock_config_percent_first_buy
        
        print(f'Bắt đầu process_trading: {symbol}')
        is_block_buy_stock = overview_config.is_block_buy
        is_block_sell_stock = overview_config.is_block_sell
        stock_id = trading_config.stock_id
        # Get stock balance 
        res_stock_balance = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
        stock_balance = res_stock_balance.get('stock_balance', {}).get('actual_vol', 0) if res_stock_balance else 0
        ceil_price = res_stock_balance.get('stock_balance', {}).get('ceil_price', 0) if res_stock_balance else 0
        symbols_existing = res_stock_balance.get('symbols_existing', []) if res_stock_balance else []
        cash_balance = handle_cash_balance_service(user_name, account, request_url, session, '')
        cash_available = cash_balance['cash_available']
    #HANDLE BUY
        if not is_block_buy_stock:
            # Tải dữ liệu
            vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                stock=stock, 
                vnindex_stock=vnindex_stock, 
                trading_chart_type=trading_chart_type, 
                following_chart_type=following_chart_type
            )
            sales_data = download_sales_volume(symbol=symbol)
            if sales_data is None:
                print(f'❌ Download sales_data cho {symbol} không thành công sau 3 lần thử!')
                message_download = f'⚠️ Download sales_data to buy symbol {symbol} failed after 3 attempts. Skipping!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)  
                return
            elif stock_data_following is None:
                print(f'❌ Download following_data cho {symbol} không thành công!')
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

            is_use_vnindex_following = following_config.is_use_vnindex_config
            is_use_vnindex_trading = trading_config.is_use_vnindex_config

            print(f'bắt đầu hàm should buy {symbol}')
            is_buy_following, is_buy, buy_reason = should_buy(
                        trading_config = trading_config,
                        following_config = following_config,
                        data_following_df = stock_data_following,
                        data_trading_df = stock_data_trading,            
                        config_type = 'stock_config'
                    )  
                    
            messages_to_buy_vnindex = ''
            if is_use_vnindex_following:
                is_buy_vnindex, buy_reason_vnindex = should_buy_following(
                    following_config = following_config,
                    data_following_df = vnindex_data_following,
                    config_type = 'vnindex_config'
                )
                messages_to_buy_vnindex = render_message(
                buy_reason_vnindex, trading_chart_value=trading_candle, following_chart_type=following_candle)
                if not is_buy_vnindex:
                    is_buy = is_buy_vnindex  

            logger.info(f'check is_buy {symbol}: {is_buy}')
            logger.info(f'check buy_reason {symbol} {buy_reason}')     

            number_order = trading_config.stock_config_number_pid_buy_once_time

            if is_buy:
                status_buy = SignalTelegramEnum.BUY_SUCCESS
            else:
                status_buy = SignalTelegramEnum.BUY_FAILED
            messages_to_buy = render_message(
                buy_reason, trading_chart_value=trading_candle, following_chart_type=following_candle)
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
                "message": messages_to_buy,
                "message_vnindex": messages_to_buy_vnindex,
                "start_time_order": start_time_order,
            }
            if is_buy_following and not is_buy:
                send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)              
            is_send_order_buy = False   
            if status_buy == SignalTelegramEnum.BUY_SUCCESS:
                # print(f'bắt đầu hàm đặt lệnh buy {symbol}')
                cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Các lệnh mua cũ còn tồn', "B")
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
                volume_by_balance =  int(volume_to_buy - stock_balance)
                volume = int(round(volume_to_buy * percent_first_buy / 100) * 100) if volume_by_balance > int(volume_to_buy*percent_first_buy) else volume_by_balance

                if cash_available < volume*start_price:
                    print('roi vao truong hop khong du tien mua theo yeu cau nen mua het so tien con lai')
                    volume = cash_available/start_price
                    volume = int(volume // 100 * 100)
                buy_order_overrall_attrs = {
                    'user_account': account,
                    'stock': symbol,
                    'volume': volume,
                    'level': level,
                    'start_price': round(start_price, 2),
                    'limit_price': round(start_price - add_price_buy + slippage_buy, 2),
                    "current_price": round(price_current, 2),
                    'step_price': step_price,
                    "slippage_buy": slippage_buy,
                    "add_price_buy": add_price_buy, 
                    "sleeping_time_buy": sleeping_time_buy,                   
                    'number_order': int(number_order),
                    'start_time_order': start_time_order
                }
                buy_messages = []
                buy_messages.append({'status_signal': SignalTelegramEnum.BUY_ORDER_OVERRAL,
                                **buy_order_overrall_attrs })  
                        
                # Xử lý mua nhạy cảm 
                if volume >=100 and trading_config.stock_config_is_mode_sensitive_buy:
                    sensitive_percentage = trading_config.stock_config_percent_sensitive_buy
                    volume_buy_sensitive = round_to_nearest_hundred(float(volume) * sensitive_percentage)
                    buy_order_attrs_send = {
                        'stock': symbol,
                        'price': round(float(high_last_row - add_price_buy), 2) if round(float(high_last_row - add_price_buy), 2) > floor_price else round(floor_price, 2),
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
                        print(f"Lệnh mua nhạy cảm handle_buy_service  của {symbol} có phản hồi là rỗng") 
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
                            print(f"Error: lệnh mua lần thứ {i+1} hàm handle_buy_service  của {symbol} có phản hồi là rỗng") 
                        volume -= volume_buy  
        
                # Send telegram tổng hợp khi thực hiện đặt xong các lệnh bán
                if is_send_order_buy:                    
                    send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)              
                    send_telegram_message_batch(user, MessageTypeEnum.OVERALL, buy_messages)
                # Send telegram hành động
                    send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_buy, **buy_attrs)              
                    send_telegram_message_batch(user, MessageTypeEnum.ACT, buy_messages)
                # print(f'kết thúc hàm đặt lệnh buy {symbol}')        
            
            # Update buy order
            if is_send_order_buy:  
                ConfigurationServices.update_is_trading_configuration(user, stock_id, True)             
                limited_times = time_to_buy // sleeping_time_buy
                limited_price_to_buy = start_price - add_price_buy + slippage_buy                
                for i in range(int(limited_times) - 1):
                    time.sleep(sleeping_time_buy)
                    res_stock = handle_stock_balance_service(user_name, account, symbol, request_url, session, asp_net_session, 'B')
                    number_stock_existing = res_stock.get('number_stock_existing', 0) if res_stock else 0
                    print('bat dau sưa lenh mua lan thu ', i+1, 'cua stock ', symbol)
                    symbols_existing = res_stock.get('symbols_existing', []) if res_stock else []
                    limit_number_stocks = vps_account.limit_number_stocks
                    if number_stock_existing >= limit_number_stocks and symbol not in symbols_existing:
                        print(f'Vượt quá giới hạn cổ phiếu tối đa, hủy lệnh mua {symbol}!')
                        cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Vượt quá giới hạn cổ phiếu tối đa', "B")
                        break

                    # Tải dữ liệu
                    vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type, 
                        following_chart_type=following_chart_type
                    )
                    sales_data = download_sales_volume(symbol=symbol)
                    if sales_data is None:
                        print(f'❌ Download sales_data sửa lệnh cho {symbol} không thành công sau 3 lần thử!')
                        message_download = f'⚠️ Download sales_data to update buy order symbol {symbol} failed after 3 attempts. Skipping!'
                        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)  
                        return
                    elif stock_data_following is None:
                        print(f'❌ Download following_data cho {symbol} không thành công!')
                        message_download = f'⚠️ Download following to update buy order symbol {symbol} failed. Skipping!'
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

                    is_use_vnindex_following = following_config.is_use_vnindex_config
                    is_use_vnindex_trading = trading_config.is_use_vnindex_config
                    is_buy, reason_buy = should_buy_following(following_config, stock_data_following, 'stock_config')                    
                    message_vnindex = ''
                    if is_use_vnindex_following:
                        is_buy_vnindex, reason_vnindex = should_buy_following(following_config, vnindex_data_following, 'vnindex_config')
                        message_vnindex = render_message(reason_vnindex, trading_candle, following_candle)
                        print(f'check is_buy_vnindex_to_update {symbol}', is_buy_vnindex)
                        if not is_buy_vnindex:
                            is_buy = False

                    print(f'is_buy_update is_buy {symbol}', is_buy)
                    price_current = stock_data_trading.iloc[-1]['close']
                    if is_buy:
                        status_buy = SignalTelegramEnum.BUY_SUCCESS
                        message_update = update_buy_order(
                            user_name, account, symbol, request_url, session, asp_net_session, "B",
                            step_price, limited_price_to_buy, i + 1
                        )
                        if message_update:
                            send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                            send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                        else:
                            break
                    else:
                        status_buy = SignalTelegramEnum.BUY_FAILED_UPDATE
                        print(f'Điều kiện sửa lệnh mua không thỏa mãn, hủy lệnh mua {symbol}!')
                        message_reason = render_message(reason_buy, trading_candle, following_candle)
                        buy_attrs = {
                            "user_account": account,
                            "platform_trading": "Smart One",
                            "stock": stock.name,
                            "level": level,
                            "price":round(price_to_start, 2),
                            "message": message_reason,
                            "message_vnindex": message_vnindex
                        }
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_buy, **buy_attrs)
                        send_telegram_message(user, MessageTypeEnum.ACT, status_signal=status_buy, **buy_attrs)
                        cancel_buy_order(user, user_name, account, symbol, request_url, session, 'Điều kiện mua không còn thỏa mãn ', "B")
                        break                        
                #Tổng kết các lệnh đã khớp theo symbol để send telegram   
                res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'B') 
                if res_matcheds:
                    print(f'danh sách các lệnh mua {symbol} đã khớp: ', res_matcheds )
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

            ConfigurationServices.update_is_trading_configuration(user, stock_id, False)

    #HANDLE SELL
        if not is_block_sell_stock and symbol in symbols_existing:
            # print(f'bắt đầu hàm thực hiện sell {symbol}')
            # Handle take profit
            volume_balance = (stock_balance // 100) * 100
            use_take_profit_first_part = trading_config.stock_config_use_take_profit_first_part
            use_take_profit_first_part_two = trading_config.stock_config_use_take_profit_first_part_two
            use_bolinger_a_part_to_take_profit = trading_config.stock_config_use_bolinger_a_part_to_take_profit
            percentage_loss = res_stock_balance.get('stock_balance', {}).get('percentage_loss', 0) if res_stock_balance else 0            
            percent_take_profit_sell_first = trading_config.stock_config_percent_take_profit_sell_first*100
            percent_take_profit_sell_first_two = trading_config.stock_config_percent_take_profit_sell_first_two*100
            percent_take_profit_sell_second = trading_config.stock_config_percent_take_profit_sell_second
            percent_take_profit_sell_second_two = trading_config.stock_config_percent_take_profit_sell_second_two
            use_take_profit_trigger = trading_config.stock_config_use_take_profit_trigger
            take_profit_percent = trading_config.stock_config_take_profit_percent
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
            if stock_data_trading is None:
                print('Download data không thành công, bỏ qua!')
                message_download_sell = f'Download data symbol {symbol } to sell không thành công. Bỏ qua lượt trade này!'
                send_message_telegram(user, MessageTypeEnum.OVERALL, message_download_sell)                 
                return
            price_current = stock_data_trading.iloc[-1]['close']    
            upper_bolinger = stock_data_following.iloc[-1]['upper_bolinger']
            is_take_profit_by_bolinger = False
            take_profit_type = ''
            if  ( (percentage_loss >= take_profit_percent and use_take_profit_trigger) 
                 or (use_take_profit_first_part_two and percentage_loss >= percent_take_profit_sell_first_two) 
                 or (use_take_profit_first_part and percentage_loss >= percent_take_profit_sell_first)
                ):
                # Chốt lãi khi giá hiện tại tăng so với giá vốn 
                is_take_profit, percent_take_profit, messages_take_profit = should_sell_take_profit(symbol, trading_config, percentage_loss)
                take_profit_type = (
                    'Bán lần 1 theo phần trăm lời'
                    if use_take_profit_first_part
                    else ('Bán lần 2 theo phần trăm lời' if use_take_profit_first_part_two else 'Bán hết theo phần trăm lời')
                )
            elif price_current >= upper_bolinger:
                # Chốt lãi khi giá hiện tại chạm bolllinger    
                is_take_profit, percent_take_profit, messages_take_profit = should_take_profit_bolinger(symbol, trading_config, price_current, upper_bolinger )
                take_profit_type = 'Bán một phần khi chạm bollinger trên'              
                if is_take_profit:
                    is_take_profit_by_bolinger = True
            volume_take_profit = int(volume_balance*percent_take_profit)
            volume_take_profit = ((volume_take_profit + 99) // 100) * 100     
            is_trading_take_profit = False
            is_sell, sell_reason = False, ''
            if is_take_profit:
                ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
                send_message_telegram(user, MessageTypeEnum.OVERALL, messages_take_profit)
                send_message_telegram(user, MessageTypeEnum.ACT, messages_take_profit)
                start_time = datetime.now()
                end_time = start_time + timedelta(hours=5)
                status_sell = SignalTelegramEnum.TAKE_PROFIT_FAILED
                while datetime.now() < end_time:
                    # Tải dữ liệu
                    vnindex_data_trading, vnindex_data_following, stock_data_trading, stock_data_following = download_data(
                        stock=stock, 
                        vnindex_stock=vnindex_stock, 
                        trading_chart_type=trading_chart_type_sell, 
                        following_chart_type=following_chart_type_sell,
                    )
                    if stock_data_trading is None:
                        print('Download data không thành công, bỏ qua!')
                        message_download = f'Không tải được dữ liệu mã {symbol}, hủy bán chốt lời lượt chạy này!'
                        send_message_telegram(user, MessageTypeEnum.OVERALL, message_download)
                        send_message_telegram(user, MessageTypeEnum.ACT, message_download)
                        break
                    print('Download data thành công!')
                    is_sell, sell_reason = should_sell_trading(
                        trading_config=trading_config,
                        data_trading_df=stock_data_trading,            
                        config_type='stock_config'
                    )
                    if is_sell:
                        is_trading_take_profit = True            
                        break
                    else:
                        status_sell = SignalTelegramEnum.TAKE_PROFIT_FAILED
                        messages_to_sell = render_message(
                            sell_reason, trading_chart_value=trading_candle_sell, following_chart_type=following_candle_sell
                        )
                        take_profit_attrs = {
                            "user_account": account,
                            "stock": stock.name,
                            "message": messages_to_sell,
                        }
                        send_telegram_message(user, MessageTypeEnum.OVERALL, status_signal=status_sell, **take_profit_attrs) 
                    time.sleep(60)  
            else:
                is_sell_following, is_sell, sell_reason = should_sell(
                    trading_config=trading_config,
                    following_config=following_config,
                    data_following_df = stock_data_following,
                    data_trading_df = stock_data_trading,            
                    config_type = 'stock_config'
                )
                # print(f'check is_sell {symbol}', is_sell) 
                # print(f'check sell_reason {symbol}', sell_reason)

            if is_trading_take_profit:
                status_sell = SignalTelegramEnum.TAKEPROFIT
            elif is_sell:
                status_sell = SignalTelegramEnum.SELL_SUCCESS
            else:
                status_sell = SignalTelegramEnum.SELL_FAILED
            #Tiến hành các bước kế tiếp
            messages_to_sell = render_message(
                sell_reason, trading_chart_value=trading_candle_sell, following_chart_type=following_candle_sell)
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
                
            is_send_order_sell = False   

            if status_sell in [SignalTelegramEnum.SELL_SUCCESS, SignalTelegramEnum.TAKEPROFIT]:
                print(f'bắt đầu hàm đặt lệnh sell {symbol}')                
                # print(f'Check sell_reason {symbol}: ', sell_reason)
                #Hủy tất cả các lệnh nếu còn đặt
                cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lệnh bán cũ còn tồn', "S")

                timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                last_row = stock_data_trading.iloc[-1]
                open_last_row = last_row['open']
                close_last_row = last_row['close']
                low_last_row = last_row['low']
                high_last_row = last_row['high']
                step_price = trading_config.stock_config_slippage_volume_sell_per_pid
                # print(f'check step_price stock {symbol}: ', step_price)
                sleeping_time_sell= trading_config.stock_config_time_update_pid_sell
                sleeping_time_sell = sleeping_time_sell if sleeping_time_sell > 5 else 5
                time_to_sell = trading_config.stock_config_time_to_sell
                time_to_sell = time_to_sell if time_to_sell >= 30 else 30    
                # print(f'check time_to_buy stock {symbol}: ', time_to_sell)
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
                    'volume': volume,
                    'start_price': round(start_price, 2),
                    'limit_price': round(start_price + add_price_sell - slippage_sell, 2),
                    "current_price": round(price_current, 2),
                    'step_price': step_price,
                    "slippage_sell": slippage_sell,
                    "add_price_sell": add_price_sell,
                    "sleeping_time_sell": sleeping_time_sell, 
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
                        sell_order_attrs_send = {
                            'stock': symbol,
                            'price': round(float(low_last_row + add_price_sell), 2) if round(float(low_last_row + add_price_sell), 2) < ceil_price else round(ceil_price, 2) , 
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
                            print(f"Error: lệnh bán nhạy cảm handle_sell_service  của {symbol} phản hồi là rỗng") 
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
                                print(f"Error: lệnh bán lần thứ {i+1} hàm handle_sell_service  của {symbol} có phản hồi là rỗng") 
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
                print('kết thúc hàm đặt lệnh sell')
               
            # Xử lý sửa lệnh
            if is_send_order_sell:
                ConfigurationServices.update_is_trading_configuration(user, stock_id, True)
                time.sleep(sleeping_time_sell)
                limited_times = time_to_sell // sleeping_time_sell
                limited_price_to_sell = start_price + add_price_sell - slippage_sell
                print(f'check limit_price_to_sell {symbol}: ', limited_price_to_sell)
                
                for i in range(int(limited_times) - 1):
                    times_update = i + 1
                    message_update = update_sell_order(user_name, account, symbol, request_url, session, asp_net_session, "S", step_price, limited_price_to_sell, times_update)
                    if message_update:
                        send_telegram_message_batch(user, MessageTypeEnum.OVERALL, message_update)
                        send_telegram_message_batch(user, MessageTypeEnum.ACT, message_update)
                    else:
                        cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Lỗi không sửa được lệnh bán', "S")
                        break           
                    time.sleep(sleeping_time_sell) 

                else:
                    # Vòng for chạy hết mà không gặp break (tức là số vòng chạy đạt limited_times
                    cancel_sell_order(user, user_name, account, symbol, request_url, session, 'Vượt quá thời gian tối đa đặt lệnh bán', "S")
                    pass
            #Tổng kết các lệnh đã khớp theo symbol để send telegram           
                res_matcheds = handle_orders_matched(user_name, account, symbol, request_url, session, '', 'S')
                if res_matcheds:
                    print(f'danh sách các lệnh bán {symbol} đã khớp: ', res_matcheds )
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
                    print('Tiến hành đóng chốt lãi một phần cho 2 loại ....') 
                    ConfigurationServices.update_use_bolinger_to_take_profit_a_part_false(user, stock_id)
                    ConfigurationServices.update_use_take_profit_first_part_false(user, stock_id, use_take_profit_first_part )

            ConfigurationServices.update_is_trading_configuration(user, stock_id, False)                        

        logger.info(f'Kết thúc process_trading: {symbol}')
    except Exception as e:
        print(f"Error in {current_thread_name}: {str(e)}")
    finally:
        # Đóng connection của thread hiện tại
        from django.db import connection
        connection.close()


def  trading_configurations(user: User, configurations: object, vps_account: Account, percent_buy_trade: float) -> None:
    print('Job trading_configurations is running...')

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
        trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
        trading_candle_sell = getattr(getattr(trading_config, "candle_sell", None), "candle_sell", "M5")
        following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
        following_candle_sell = getattr(getattr(following_config, "candle_sell", None), "candle_sell", "D1")

        # Xác định kiểu biểu đồ dựa trên enum (có thể điều chỉnh theo logic cụ thể)
        trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
        trading_chart_type_sell = getattr(CandleEnum, trading_candle_sell, CandleEnum.M5)
        following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
        following_chart_type_sell = getattr(CandleEnum, following_candle_sell, CandleEnum.D1)
        prepared_configs.append({
            "trading_candle": trading_candle,
            "trading_candle_sell": trading_candle_sell,
            "following_candle": following_candle,
            "following_candle_sell": following_candle_sell,
            "trading_chart_type": trading_chart_type,
            "trading_chart_type_sell": trading_chart_type_sell,
            "following_chart_type": following_chart_type,
            "following_chart_type_sell": following_chart_type_sell,
            "stock": stock,
            "trading_config": trading_config,
            "following_config": following_config,
            "overview_config": overview_config,
        })

    # Hàm worker cho mỗi cấu hình
    def worker(prepared):
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
            from django.db import connection
            connection.close()

    # Sử dụng ThreadPoolExecutor với tối đa 100 worker (thread)
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for config in prepared_configs:
            try:
                futures.append(executor.submit(worker, config))
                time.sleep(0.2)  # Thêm độ trễ giữa các luồng
            except RuntimeError as e:
                print(f"Cannot submit new task: {e}")
                break  # Dừng nếu executor đã shutdown

        # Chờ các task hoàn thành và xử lý ngoại lệ (nếu có)
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread: {e}")

    
def trading(user: User, vps_account: Account, symbol: str) -> None:
    print('Job trading is running...')
    
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
    configurations_handle_trading = [
        config for config in user_configurations
        if (trading_config := config.get("trading_config")) and trading_config.is_trading is False
    ]
    list_symbol_not_trading  = [
        config["stock"].name
        for config in configurations_handle_trading
    ]
    # print('List symbol_not_trading: ', list_symbol_not_trading )

    # Get stock balance 
    res_stock_balance = handle_stock_balance_service(account_name, account_num, '', request_url, session_id, '','' )
    stock_balance = res_stock_balance.get('stock_balance', {}).get('actual_vol', 0) if res_stock_balance else 0
    number_stock_existing = res_stock_balance.get('number_stock_existing', 0) if res_stock_balance else 0
    percent_buy_trade = res_stock_balance.get('percent_buy_trade', 0) if res_stock_balance else 0
    symbols_existing = res_stock_balance.get('symbols_existing', []) if res_stock_balance else []
    # print('List symbols_existing: ', symbols_existing )
    # print('Check number_stock_existing: ', number_stock_existing )
    # print('Check limit_number_stocks: ', limit_number_stocks )
    configurations_test_trading = [
        config for config in configurations_handle_trading
        if (stock := config.get("stock")) and stock.name in ['CII', 'HCM', 'DIG'] ]
    if number_stock_existing >= limit_number_stocks:
        configurations_handle_trading = [
            config for config in configurations_handle_trading
            if (stock := config.get("stock")) and stock.name in symbols_existing ]
    list_symbols_process_trading  = [
        config["stock"].name
        for config in configurations_handle_trading
    ]
    logger.info(f'List list_symbols_process_trading của user {user.username} : {list_symbols_process_trading} ')
    list_symbols_test_trading  = [
        config["stock"].name
        for config in configurations_test_trading
    ]
    trading_configurations(user, configurations_handle_trading, vps_account, percent_buy_trade)


def trading_request(user: User, vps_account: Account, stock_id: str, symbol: str, request_buy: bool, request_sell: bool, volume_sell: str) -> bool:
    print('Job request trading is running...')

    vnindex_stock = StockService.get_stock_by_symbol('VNINDEX')
    limit_number_stocks = vps_account.limit_number_stocks
    prepared_configs = []

    configuration = ConfigurationServices.get_user_configuration_by_stock_symbol(user=user, stock_symbol=symbol)
    trading_config = configuration.get("trading_config", {})
    following_config = configuration.get("following_config", {})
    overview_config = configuration.get("overview_config", {})

    stock = configuration.get("stock")

    trading_candle = getattr(getattr(trading_config, "candle", None), "candle", "M5")
    trading_candle_sell = getattr(getattr(trading_config, "candle_sell", None), "candle_sell", "M5")
    following_candle = getattr(getattr(following_config, "candle", None), "candle", "D1")
    following_candle_sell = getattr(getattr(following_config, "candle_sell", None), "candle_sell", "D1")

    trading_chart_type = getattr(CandleEnum, trading_candle, CandleEnum.M5)
    trading_chart_type_sell = getattr(CandleEnum, trading_candle_sell, CandleEnum.M5)
    following_chart_type = getattr(CandleEnum, following_candle, CandleEnum.D1)
    following_chart_type_sell = getattr(CandleEnum, following_candle_sell, CandleEnum.D1)

    prepared_configs.append({
        "trading_candle": trading_candle,
        "trading_candle_sell": trading_candle_sell,
        "following_candle": following_candle,
        "following_candle_sell": following_candle_sell,
        "trading_chart_type": trading_chart_type,
        "trading_chart_type_sell": trading_chart_type_sell,
        "following_chart_type": following_chart_type,
        "following_chart_type_sell": following_chart_type_sell,
        "stock": stock,
        "trading_config": trading_config,
        "following_config": following_config,
        "overview_config": overview_config,
    })

    def run_process_buy():
        process_buy_request(
            prepared_configs[0], user, vnindex_stock, vps_account, stock_id, limit_number_stocks, request_buy, request_sell
        )

    def run_process_sell():
        process_sell_request(
            prepared_configs[0], user, vnindex_stock, vps_account, stock_id, limit_number_stocks, request_buy, request_sell, volume_sell
        )

    if prepared_configs:
        print('check length prepared_configs: ', len(prepared_configs))
        if request_buy:
            threading.Thread(target=run_process_buy).start()
            return True
        elif request_sell:
            threading.Thread(target=run_process_sell()).start()
            return True
    else:
        print("Không có dữ liệu trong prepared_configs, bỏ qua process_trade_request.")
        return False

