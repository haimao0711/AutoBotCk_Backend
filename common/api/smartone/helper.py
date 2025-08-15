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
    if response_code == 1:
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


def extract_buy_object(object: OrderData):
    volume = int(object[0]['volume'])
    matchVolume = int(object[0]['matchVolume'])
    if matchVolume > 0:
        if volume == matchVolume:
            status = 'Khớp'
        else:
            status = 'Khớp một phần'
    else:
        status = 'Chưa khớp'
    return {
        'symbol': object[0]['symbol'],
        'volume': object[0]['volume'],
        'price': float(object[0]['showPrice']),
        'account': object[0]['accountCode'],
        'order_num': object[0]['orderNo'],
        'time': object[0]['orderTime'],
        'ref_id': object[0]['refID'],
        'status': status,
        'type': SideOrderEnum.BUY,
        'channel': object[0]['channel']
    }


def extract_sell_object(object: OrderData):
    volume = int(object[0]['volume'])
    matchVolume = int(object[0]['matchVolume'])
    if matchVolume > 0:
        if volume == matchVolume:
            status = 'Khớp'
        else:
            status = 'Khớp một phần'
    else:
        status = 'Chưa Khớp'
    return {
        'symbol': object[0]['symbol'],
        'volume': object[0]['volume'],
        'price': float(object[0]['showPrice']),
        'account': object[0]['accountCode'],
        'order_num': object[0]['orderNo'],
        'time': object[0]['orderTime'],
        'ref_id': object[0]['refID'],
        'status': status,
        'type': SideOrderEnum.SELL,
        'channel': object[0]['channel']
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


def extract_stock_balance_object(object: list):
    return {
        'symbol': object[0]['symbol'],
        'account': object[0]['account'],
        'avg_price': float(object[0]['avg_price']),
        'ceil_price': float(object[0]['ceil_price']),
        'floor_price': float(object[0]['floor_price']),
        'actual_vol': float(object[0]['actual_vol']),
        'available_vol': float(object[0]['avaiable_vol']),
        'value': float(object[0]['value']),
        'buy_t0': float(object[0]['buy_t0']),
        'sell_t0': float(object[0]['sell_t0']),
        'buy_t1': float(object[0]['buy_t1']),
        'sell_t1': float(object[0]['sell_t1']),
        'buy_t2': float(object[0]['buy_t2']),
        'sell_t2': float(object[0]['sell_t2']),
        'oneday_avg_price': float(object[0]['oneday_avg_price']),
        'percentage_loss': float(object[0]['gain_loss_per'].rstrip('%')),
        'value_loss': float(object[0]['gain_loss_value']),
    }


# def extract_cash_balance_object(object: CashData):
#     return {
#         'symbol': 'VND',
#         'cash_balance': float(object['cash_balance']),  # tiền mặt có thể rút VND
#         'total_assets': float(object['total_asset']),  # tài sản ròng
#         'cash_available': float(object['ee_available_tk']) # hạn mức ứng tiền
#     }

def extract_cash_balance_object(object: CashData): 
    return {
        'symbol': 'VND',
        'cash_balance': float(object.get('cash_balance', 0)),   # tiền mặt có thể rút VND
        'total_assets': float(object.get('total_asset', 0)),    # tài sản ròng
        'cash_available': float(object.get('ee_available_tk', 0))  # hạn mức ứng tiền
    }
