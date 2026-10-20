from common.api.smartone.enums import ResponseAPISmartOneEnum
import json
import time
import logging

logger = logging.getLogger(__name__)

from common.api.smartone.api import (buy_stock_smart_one, cancel_order_smart_one, get_cash_balance, get_stock_balance, get_account_status,
                 get_transaction, get_orders_status, sell_stock_smart_one, update_order_smart_one)
from common.api.smartone.helper import (extract_buy_object, extract_cancel_order_object, extract_cash_balance_object,
                    extract_sell_object, extract_stock_balance_object, extract_transacion_object,
                    extract_update_order_object, request_new_session, validate_response)


def _safe_parse_json(text: str, context: str, fallback):
    """
    Parse JSON an toàn.
    - Nếu server trả về HTML (lỗi tạm thời): log error và trả về fallback.
    - Nếu JSON không hợp lệ: log error và trả về fallback.
    - Trả về (object, True) nếu thành công, (fallback, False) nếu thất bại.
    """
    if text.strip().startswith('<'):
        logger.error(f"[{context}] Server trả về HTML thay vì JSON (server đang lỗi/session hết hạn) | Preview: {text[:200]}")
        return fallback, False
    try:
        return json.loads(text), True
    except json.JSONDecodeError as e:
        logger.error(f"[{context}] Lỗi giải mã JSON: {e} | Dữ liệu: {text[:200]}")
        return fallback, False


def handle_buy_service(user_account: str, trade_account: str, url: str, symbol: str, session: str,
                        asp_net_session: str, price: float, volume: float, ref_id: str):
    
    buy_res = buy_stock_smart_one(
        user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id)
    if buy_res is None:
        logger.error(f"API Buy Error: Không nhận được phản hồi từ máy chủ cho {symbol}")
        return {}
    buy_text = buy_res.text
    if not buy_text:
        logger.error(f"API Buy Error: Phản hồi rỗng từ máy chủ cho {symbol}")
        return {}
    buy_object, ok = _safe_parse_json(buy_text, f"buy_stock/{symbol}", {})
    if not ok:
        return {}
    response_type = validate_response(buy_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = buy_object['data']
        return extract_buy_object(object=data)

    else:
        logger.error(f"API Buy Error: {buy_object.get('rs')} (rc: {buy_object.get('rc')}) for {symbol}")
        request_new_session()
        return {"error": buy_object.get('rs'), "rc": buy_object.get('rc')}


def handle_sell_service(user_account: str, trade_account: str, url: str, symbol: str, session: str, asp_net_session: str, price: float, volume: float, ref_id: str):
    sell_res = sell_stock_smart_one(
        user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id)
    if sell_res is None:
        logger.error(f"API Sell Error: Không nhận được phản hồi từ máy chủ cho {symbol}")
        return {}
    sell_text = sell_res.text
    if not sell_text:
        logger.error(f"API Sell Error: Phản hồi rỗng từ máy chủ cho {symbol}")
        return {}
    sell_object, ok = _safe_parse_json(sell_text, f"sell_stock/{symbol}", {})
    if not ok:
        return {}
    response_type = validate_response(sell_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = sell_object.get('data', [])
        return extract_sell_object(object=data)
    else:
        logger.error(f"API Sell Error: {sell_object.get('rs')} (rc: {sell_object.get('rc')}) for {symbol}")
        request_new_session()
        return {"error": sell_object.get('rs'), "rc": sell_object.get('rc')}


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
        if res is None:
            return ResponseAPISmartOneEnum.FAILED, {}
        res_text = res.text
        if not res_text:
            logger.error(f"API Update Order Error: Phản hồi rỗng cho {symbol}")
            return ResponseAPISmartOneEnum.FAILED, {}
        obj, ok = _safe_parse_json(res_text, f"update_order/{symbol}", {})
        if not ok:
            return ResponseAPISmartOneEnum.FAILED, {}
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
    if cancel_order_res is None:
        logger.error("API Cancel Error: Không nhận được phản hồi từ máy chủ")
        return {}
    cancel_order_text = cancel_order_res.text
    if not cancel_order_text:
        logger.error("API Cancel Error: Phản hồi rỗng từ máy chủ")
        return {}
    cancel_order_object, ok = _safe_parse_json(cancel_order_text, "cancel_order", {})
    if not ok:
        return {}
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
        logger.error("Không nhận được phản hồi từ API get_orders_status (PENDING).")
        return None
    data_text = data_res.text
    if not data_text:
        logger.error("API get_orders_status (PENDING) trả về dữ liệu rỗng")
        return None
    data_object, ok = _safe_parse_json(data_text, "get_orders_status/PENDING", None)
    if not ok:
        return None
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
        return None

def handle_orders_matched(user_account, trade_account, symbol, url, valid_session, asp_net_session, side):   
    data_res = get_orders_status(
        user_account, trade_account, url, valid_session, asp_net_session, "MATCH" )
    if data_res is None:
        logger.info("Không nhận được phản hồi từ API get_orders_status (MATCH).")
        return []
    data_text = data_res.text
    if not data_text:
        logger.error("API get_orders_status (MATCH) trả về dữ liệu rỗng")
        return []
    data_object, ok = _safe_parse_json(data_text, "get_orders_status/MATCH", [])
    if not ok:
        return []
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
                "orderTime": order.get("orderTime", ""),
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
    if transaction_res is None:
        logger.error("API Transaction Error: Không nhận được phản hồi từ máy chủ")
        return []
    transaction_text = transaction_res.text
    if not transaction_text:
        logger.error("API Transaction Error: Phản hồi rỗng từ máy chủ")
        return []
    transaction_object, ok = _safe_parse_json(transaction_text, "get_transaction", [])
    if not ok:
        return []
    response_type = validate_response(transaction_object)

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
    if cash_balance_res is None:
        logger.error("API Cash Balance Error: Không nhận được phản hồi từ máy chủ")
        return {}
    cash_balance_text = cash_balance_res.text
    if not cash_balance_text:
        logger.error("API Cash Balance Error: Phản hồi rỗng từ máy chủ")
        return {}
    cash_balance_object, ok = _safe_parse_json(cash_balance_text, "get_cash_balance", {})
    if not ok:
        return {}
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
    if stock_balance_res is None:
        logger.error("API Stock Balance Error: Không nhận được phản hồi từ máy chủ")
        return {}
    stock_balance_text = stock_balance_res.text
    if not stock_balance_text:
        logger.error("API Stock Balance Error: Phản hồi rỗng từ máy chủ")
        return {}
    stock_balance_object, ok = _safe_parse_json(stock_balance_text, "get_stock_balance", {})
    if not ok:
        return {}
    response_type = validate_response(stock_balance_object)

    if response_type == ResponseAPISmartOneEnum.SUCCESS:
        data = stock_balance_object.get('data', [])
        if not isinstance(data, list):
            logger.warning(f"API Stock Balance Warning: 'data' không phải là danh sách cho {symbol}")
            data = []
            
        list_stock_existing = [
            item for item in data 
            if isinstance(item, dict) and str(item.get("actual_vol", "0")) != '0' and item.get("symbol") != "TOTAL"
        ]
        
        # tính tổng actual_vol và avaiable_vol
        total_volume_buy = sum(int(item.get("actual_vol", 0)) for item in list_stock_existing if str(item.get("actual_vol")).isdigit())
        total_volume_trade = sum(int(item.get("avaiable_vol", 0)) for item in list_stock_existing if str(item.get("avaiable_vol")).isdigit())
        
        percent_buy_trade = (total_volume_trade / total_volume_buy * 100) if total_volume_buy else 0
        list_symbols_existing = [item.get("symbol") for item in list_stock_existing if item.get("symbol")]
        number_stock_existing = len(list_stock_existing)
        
        stock_balance_by_symbol = [item for item in data if isinstance(item, dict) and item.get("symbol") == symbol]
        
        if stock_balance_by_symbol:
            stock_balance = extract_stock_balance_object(stock_balance_by_symbol[0])            
        else:
            stock_balance = {
                'available_vol': 0,
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
        logger.error(f"API Stock Balance Error: {stock_balance_object.get('rs')} (rc: {stock_balance_object.get('rc')})")
        request_new_session()
        return {}


def validate_session(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str, retries: int = 2):
    # Retry để tránh false-positive "session hết hạn" do API timeout hoặc server trả về HTML lỗi tạm thời
    account_status_res = None
    for attempt in range(retries + 1):
        account_status_res = get_account_status(
            user_account, trade_account, url, session, asp_net_session)
        print(f"account_status_res: {account_status_res}")
        # Trường hợp 1: timeout hoàn toàn (None)
        if account_status_res is None:
            if attempt < retries:
                logger.warning(f"API Account Status TIMEOUT (lần {attempt + 1}/{retries + 1}), thử lại...")
                time.sleep(1)
                continue
            break

        # Trường hợp 2: server trả về HTTP lỗi (4xx, 5xx)
        if account_status_res.status_code != 200:
            if attempt < retries:
                logger.warning(f"API Account Status HTTP {account_status_res.status_code} (lần {attempt + 1}/{retries + 1}), thử lại...")
                time.sleep(1)
                continue
            break

        # Trường hợp 3: server trả về HTML thay vì JSON (server lỗi nhưng vẫn HTTP 200)
        content_type = account_status_res.headers.get('Content-Type', '')
        response_text = account_status_res.text.strip()
        if 'json' not in content_type and response_text.startswith('<'):
            if attempt < retries:
                logger.warning(f"API Account Status trả về HTML thay vì JSON (lần {attempt + 1}/{retries + 1}), thử lại... | Preview: {response_text[:100]}")
                time.sleep(1)
                continue
            # Hết retry vẫn nhận HTML → log rõ ràng
            logger.error(f"Lỗi giải mã JSON: Server trả về HTML sau {retries + 1} lần thử. | Dữ liệu nhận được: {response_text}")
            return False, {}

        # Response hợp lệ (JSON) → thoát vòng lặp
        break

    if account_status_res is None:
        logger.error("API Account Status TIMEOUT sau tất cả các lần thử")
        return False, {}

    account_status_text = account_status_res.text
    if not account_status_text:
        logger.error("API trả về dữ liệu rỗng")
        return False, {}

    try:
        account_status_object = json.loads(account_status_text)
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi giải mã JSON: {e} | Dữ liệu nhận được: {account_status_text}")
        return False, {}
    response_type = validate_response(account_status_object)

    if response_type != ResponseAPISmartOneEnum.SUCCESS:
        logger.error(f"API Account Status Error: {account_status_object.get('rs')} (rc: {account_status_object.get('rc')})")
        return False, {}

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
