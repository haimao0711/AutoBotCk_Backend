import random
from typing import Dict, Any

from common.api.smartone.type import (CancelOrderData, CashData, Order, OrderData, ResponseSmartOneType, StockData,
                  UpdateOrderData)
from common.api.smartone.enums import (ResponseAPISmartOneEnum, SideOrderEnum, StatusOrderEnum,
                   StatusTransactionEnum)

__all__ = ['convert_text_to_dict', 'validate_response', 'generate_ref_id']


def convert_text_to_dict(data_class, data: Dict[str, Any]):
    fieldtypes = {
        f.name: f.type for f in data_class.__dataclass_fields__.values()}
    return data_class(**{f: convert_text_to_dict(fieldtypes[f], data[f]) if hasattr(fieldtypes[f], '__dataclass_fields__') else data[f] for f in data})


def validate_response(object: ResponseSmartOneType) -> ResponseAPISmartOneEnum:
    response_code = object.get('rc', None)
    if response_code is not None:
        for item in ResponseAPISmartOneEnum:
            if item.value == response_code:
                return item
    return None


def generate_ref_id(user_account, type, length_ref_id=16):
    random_string = ''.join(random.choices('0123456789', k=length_ref_id))
    return f'{user_account}.{type}.{random_string}'


def handler_response(object: ResponseSmartOneType) -> object:
    pass


def request_new_session():
    pass


def extract_buy_object(object: Any):
    if not object:
        return {}
    
    # Nếu là list, lấy phần tử đầu tiên
    item = object[0] if isinstance(object, list) and len(object) > 0 else (object if isinstance(object, dict) else {})
    if not item: return {}

    volume = int(item.get('volume', 0))
    matchVolume = int(item.get('matchVolume', 0))
    if matchVolume > 0:
        status = 'Khớp' if volume == matchVolume else 'Khớp một phần'
    else:
        status = 'Chưa khớp'
        
    return {
        'symbol': item.get('symbol', ''),
        'volume': volume,
        'price': float(item.get('showPrice', 0)),
        'account': item.get('accountCode', ''),
        'order_num': item.get('orderNo', ''),
        'time': item.get('orderTime', ''),
        'ref_id': item.get('refID', ''),
        'status': status,
        'type': SideOrderEnum.BUY,
        'channel': item.get('channel', '')
    }


def extract_sell_object(object: Any):
    if not object:
        return {}
    
    item = object[0] if isinstance(object, list) and len(object) > 0 else (object if isinstance(object, dict) else {})
    if not item: return {}

    volume = int(item.get('volume', 0))
    matchVolume = int(item.get('matchVolume', 0))
    if matchVolume > 0:
        status = 'Khớp' if volume == matchVolume else 'Khớp một phần'
    else:
        status = 'Chưa Khớp'
        
    return {
        'symbol': item.get('symbol', ''),
        'volume': volume,
        'price': float(item.get('showPrice', 0)),
        'account': item.get('accountCode', ''),
        'order_num': item.get('orderNo', ''),
        'time': item.get('orderTime', ''),
        'ref_id': item.get('refID', ''),
        'status': status,
        'type': SideOrderEnum.SELL,
        'channel': item.get('channel', '')
    }


def extract_update_order_object(object: UpdateOrderData):
    return {
        'orderNo': object[0]['orderNo'],
        'status': StatusOrderEnum.UPDATE
    }


def extract_cancel_order_object(object: CancelOrderData):
    return {
        'order_number': object.orderNo,
        'status': StatusOrderEnum.CANCEL
    }


def extract_transacion_object(object: Order):

    status = ''
    status_en = object.C_STATUS_NAME_EN

    match status_en:
        case "Match":
            status = StatusTransactionEnum.MATCH
        case "Cancel":
            status = StatusTransactionEnum.CANCEL
        case _:
            status = StatusTransactionEnum.UNKNOWN

    return {
        "time": object.C_ORDER_TIME,
        "volume_order": int(object.C_ORDER_VOLUME),
        "volume_match": int(object.C_MATCH_VOL),
        "price_match": float(object.C_MATCH_PRICE),
        "fee": float(object.C_FEE_VALUE),
        "symbol": object.C_SHARE_CODE,
        "status": status
    }


def extract_stock_balance_object(object: Any):
    if not object:
        return {}
        
    item = object[0] if isinstance(object, list) and len(object) > 0 else (object if isinstance(object, dict) else {})
    if not item: return {}

    # Xử lý an toàn cho percentage_loss
    gain_loss_per = item.get('gain_loss_per', '0')
    if isinstance(gain_loss_per, str):
        gain_loss_per = gain_loss_per.rstrip('%')
    
    try:
        percentage_loss = float(gain_loss_per)
    except (ValueError, TypeError):
        percentage_loss = 0.0

    return {
        'symbol': item.get('symbol', ''),
        'account': item.get('account', ''),
        'avg_price': float(item.get('avg_price', 0)),
        'ceil_price': float(item.get('ceil_price', 0)),
        'floor_price': float(item.get('floor_price', 0)),
        'actual_vol': float(item.get('actual_vol', 0)),
        'available_vol': float(item.get('avaiable_vol', 0)),
        'value': float(item.get('value', 0)),
        'buy_t0': float(item.get('buy_t0', 0)),
        'sell_t0': float(item.get('sell_t0', 0)),
        'buy_t1': float(item.get('buy_t1', 0)),
        'sell_t1': float(item.get('sell_t1', 0)),
        'buy_t2': float(item.get('buy_t2', 0)),
        'sell_t2': float(item.get('sell_t2', 0)),
        'oneday_avg_price': float(item.get('oneday_avg_price', 0)),
        'percentage_loss': percentage_loss,
        'value_loss': float(item.get('gain_loss_value', 0)),
    }


# def extract_cash_balance_object(object: CashData):
#     return {
#         'symbol': 'VND',
#         'cash_balance': float(object['cash_balance']),  # tiền mặt có thể rút VND
#         'total_assets': float(object['total_asset']),  # tài sản ròng
#         'cash_available': float(object['ee_available_tk']) # hạn mức ứng tiền
#     }

def extract_cash_balance_object(object: any): 
    if isinstance(object, list):
        object = object[0] if object else {}
        
    return {
        'symbol': 'VND',
        'cash_balance': float(object.get('cash_balance', 0)),   # tiền mặt có thể rút VND
        'total_assets': float(object.get('total_asset', 0)),    # tài sản ròng
        'cash_available': float(object.get('ee_available_tk', 0))  # hạn mức ứng tiền
    }
