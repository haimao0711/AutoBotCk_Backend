from common.api.smartone.enums import ResponseAPISmartOneEnum
import json
import logging

logger = logging.getLogger(__name__)

from common.api.smartone.api import (buy_stock_smart_one, cancel_order_smart_one, get_cash_balance, get_stock_balance, get_account_status,
                 get_transaction, get_orders_status, sell_stock_smart_one, update_order_smart_one)
from common.api.smartone.helper import (extract_buy_object, extract_cancel_order_object, extract_cash_balance_object,
                    extract_sell_object, extract_stock_balance_object, extract_transacion_object,
                    extract_update_order_object, request_new_session, validate_response)


def handle_buy_service(user_account: str, trade_account: str, url: str, symbol: str, session: str,
                        asp_net_session: str, price: float, volume: float, ref_id: str):
    
    buy_res = buy_stock_smart_one(
        user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id)
    buy_text = buy_res.text
    buy_object = json.loads(buy_text)
    response_type = validate_response(buy_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = buy_object['data']
        return extract_buy_object(object=data)

    else:
        logger.error(f"API Buy Error: {buy_object.get('rs')} (rc: {buy_object.get('rc')}) for {symbol}")
        request_new_session()
        return {}


def handle_sell_service(user_account: str, trade_account: str, url: str, symbol: str, session: str, asp_net_session: str, price: float, volume: float, ref_id: str):
    sell_res = sell_stock_smart_one(
        user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id)
    sell_text = sell_res.text
    sell_object = json.loads(sell_text)
    response_type = validate_response(sell_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = sell_object.get('data', [])
        return extract_sell_object(object=data)
    else:
        logger.error(f"API Sell Error: {sell_object.get('rs')} (rc: {sell_object.get('rc')}) for {symbol}")
        request_new_session()
        return {}


def handle_update_order_service(user_account, trade_account, url, symbol, session,
                                asp_net_session, order_num, price, update_price,
                                update_volume, ref_id, side):
    def call_update(price_value):
        """Gọi API update order và trả về response_type + object"""
        res = update_order_smart_one(
            user_account, trade_account, url, symbol, session,
            asp_net_session, order_num, price, price_value,
            update_volume, ref_id, side
        )
        obj = json.loads(res.text)
        return validate_response(obj), obj

    # Lần gọi đầu
    response_type, update_order_object = call_update(update_price)

    # Nếu lỗi bước giá, điều chỉnh giá dựa theo side
    if response_type == ResponseAPISmartOneEnum.INVALID_STEP_PRICE_CODE:
        if side == 'B':       # Mua → cộng 0.05
            adjusted_price = update_price + 0.05
        elif side == 'S':     # Bán → trừ 0.05
            adjusted_price = update_price - 0.05
        else:                 # Khác → giữ nguyên
            adjusted_price = update_price

        response_type, update_order_object = call_update(adjusted_price)

    # Kiểm tra thành công
    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        update_order = update_order_object.get('data')
        return extract_update_order_object(update_order) if update_order else []

    # Nếu không thành công, yêu cầu phiên mới
    request_new_session()
    return []


def handle_cancel_order_service(user_account, url, session, asp_net_session, order_num, ref_id ):
    cancel_order_res = cancel_order_smart_one(
        user_account, url, session, asp_net_session, order_num, ref_id)
    cancel_order_text = cancel_order_res.text
    cancel_order_object = json.loads(cancel_order_text)
    response_type = validate_response(cancel_order_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        return cancel_order_object

    else:
        request_new_session()
        return {}

def handle_orders_not_matched(user_account, trade_account, symbol, url, valid_session, asp_net_session, side):   
    data_res = get_orders_status(
        user_account, trade_account, url, valid_session, asp_net_session, "PENDING" )
    if data_res is None:
        print("Không nhận được phản hồi từ API get_orders_status.")
        return []
    data_text = data_res.text
    try:
        data_object = json.loads(data_res.text)
    except Exception as e:
        print("Lỗi khi parse JSON từ phản hồi:", e)
        return []
    response_type = validate_response(data_object)
    
    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        not_matcheds = data_object['data']
        if side == 'All':
        # Trả về toàn bộ danh sách nếu side là 'All'
            orders_detail = [
                {
                 "orderNo": order["orderNo"],
                 "side": order["side"],  
                 "symbol": order["symbol"],
                  "showPrice": order["showPrice"],
                  "volume": order["volume"],
                  "status": 'Chưa khớp'
                }
                for order in not_matcheds
            ]
        elif symbol == 'all_order':
        # Lọc tất cả các lệnh theo side
            orders_detail = [
               {
                  "orderNo": order["orderNo"],
                  "side": order["side"],  
                   "symbol": order["symbol"],
                   "showPrice": order["showPrice"],
                    "volume": order["volume"],
                    "status": 'Chưa khớp'
               }
              for order in not_matcheds  if (order.get("side") == side)
           ]
        else:
        # Lọc theo các điều kiện đã cho
            orders_detail = [
               {
                  "orderNo": order["orderNo"],
                  "side": order["side"],  
                   "symbol": order["symbol"],
                   "showPrice": order["showPrice"],
                    "volume": order["volume"],
                    "status": 'Chưa khớp'
               }
              for order in not_matcheds 
              if (order.get("symbol") == symbol and order.get("side") == side)
           ]
        return orders_detail
    else:
        request_new_session()
        return []

def handle_orders_matched(user_account, trade_account, symbol, url, valid_session, asp_net_session, side):   
    data_res = get_orders_status(
        user_account, trade_account, url, valid_session, asp_net_session, "MATCH" )
   
    data_text = data_res.text
    data_object = json.loads(data_text)
    response_type = validate_response(data_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        orders_matcheds = data_object['data']
        orders_detail = [
            {
                "orderNo": order["orderNo"],
                "side": order["side"],  
                "symbol": order["symbol"],
                "showPrice": order["showPrice"],
                "volume": order["volume"],
                "status": 'Đã khớp'
            }
            for order in orders_matcheds if order.get("symbol") == symbol and order.get("side") == side
        ]    
        return orders_detail

    else:
        request_new_session()
        return []


def handle_transaction_service(user_account, trade_account, url, valid_session, asp_net_session, start_date=None, end_date=None):
    if start_date and end_date:
        transaction_res = get_transaction(
            user_account, trade_account, url, valid_session, asp_net_session, start_date, end_date)
    else:
        transaction_res = get_transaction(
            user_account, trade_account, url, valid_session, asp_net_session)
    if transaction_res:
        transaction_text = transaction_res.text
        transaction_object = json.loads(transaction_text)
        response_type = validate_response(transaction_object)
    else:
        pass 

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        transactions = transaction_object['data']
        matched_orders = [ order for order in transactions if order["C_MATCH_VOL"] > 0 ]
        print('danh sách các lệnh đã khớp: ', matched_orders )
        return matched_orders
        # return extract_transacion_object(object=transactions)

    else:
        request_new_session()
        return []


def handle_cash_balance_service(user_account, trade_account, url, session, asp_net_session):
    cash_balance_res = get_cash_balance(
        user_account, trade_account, url, session, asp_net_session)
    cash_balance_text = cash_balance_res.text
    cash_balance_object = json.loads(cash_balance_text)
    response_type = validate_response(cash_balance_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        cash_balance = cash_balance_object['data']
        return extract_cash_balance_object(object=cash_balance)

    else:
        request_new_session()
        return {}


def handle_stock_balance_service(user_account, trade_account, symbol, url, session, asp_net_session, side):
    stock_balance_res = get_stock_balance(
        user_account, trade_account, url, session, asp_net_session)
    stock_balance_text = stock_balance_res.text
    stock_balance_object = json.loads(stock_balance_text)
    response_type = validate_response(stock_balance_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = stock_balance_object['data']
        list_stock_existing = [item for item in data if item.get("actual_vol", 0) != '0' and item.get("symbol") != "TOTAL"]
        
        # tính tổng actual_vol và avaiable_vol
        total_volume_buy = sum(int(item.get("actual_vol", 0)) for item in list_stock_existing)
        total_volume_trade = sum(int(item.get("avaiable_vol", 0)) for item in list_stock_existing)
        percent_buy_trade = (total_volume_trade / total_volume_buy * 100) if total_volume_buy else 0
        list_symbols_existing = [item["symbol"] for item in list_stock_existing]
        number_stock_existing = int(len(list_stock_existing)) if list_stock_existing else 0
        stock_balance_by_symbol = [item for item in data if item["symbol"] == symbol]
        # print(f'data stock balance symbol {symbol}: ', stock_balance_by_symbol )
        if stock_balance_by_symbol:
            stock_balance = extract_stock_balance_object(stock_balance_by_symbol)            
        else:
            stock_balance = {'available_vol': 0,
                             'actual_vol': 0,
                             'percentage_loss': 0,
                             'ceil_price': 0,
                             'floor_price': 0,
                             }
        return {
                'number_stock_existing': number_stock_existing,
                'stock_balance': stock_balance,
                'symbols_existing': list_symbols_existing,
                'percent_buy_trade': percent_buy_trade
            }
    else:
        print('rơi vào trường hợp response_type lỗi ')
        request_new_session()
        return {}


def validate_session(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str):
    # default we use normal account

    account_status_res = get_account_status(
        user_account, trade_account, url, session, asp_net_session)
    account_status_text = account_status_res.text
    account_status_object = json.loads(account_status_text)
    response_type = validate_response(account_status_object)
    
    # print('check account_status_object: ', account_status_object)
    # print('check response_type: ', response_type)
    if response_type == None:
        return False, {}
    else:    
        data = account_status_object.get("data", {})
        if isinstance(data, list):
            data = data[0] if data else {}
        result = {
            "total_equity": int(data.get("total_equity", 0)),  # Tổng tiền hiện có
            "cash_balance": int(data.get("cash_balance", 0)),  # Số tiền mặt có thể rút
            "total_market_value": int(data.get("total_market_value", 0)),  # Giá trị cổ phiếu
            "cash_available": int(data.get("cash_avai", 0)),  # Số tiền có thể mua cổ phiếu
            "gain_loss_value": int(data.get("gain_loss_value", 0)),  # Lãi/lỗ danh mục
            "gain_loss_oneday_value": int(data.get("gain_loss_oneday_value", 0)),  # Lãi/lỗ hôm nay
        }
    return True, result

