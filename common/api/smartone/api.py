import json
import requests
from datetime import datetime, timedelta

__all__ = ['buy_stock_smart_one', 'update_order_smart_one', 'sell_stock_smart_one',
           'cancel_order_smart_one', 'get_order_book', 'get_transaction', 'get_cash_balance', 'get_stock_balance', 'validate_response']



def trade_stock_smart_one(user_account: str, trade_account: str, url: str, symbol: str, session: str,
                           asp_net_session: str, price: float, volume: float, ref_id: str, side: str):

    str_price = str(price)

    payload = json.dumps({
        "group": "O",
        "user": user_account,
        "session": session,
        "language": "vi",
        # "extInfo": "2706425978|Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "extInfo": "1167763841|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "data": {            
            "cmd": "Web.newOrder",
            "account": trade_account,
            "advance": "",
            "orderType": "1",
            "pin": "",
            "price": str_price,
            "refId": ref_id ,
            "room": "",
            "side": side,
            "symbol": symbol,  
            "type": "string",
            "volume": volume,
        }
    })
    # print(f'check payload to {side}', payload)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }
 
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        # print(f'Mã trạng thái phản hồi trade_stock_smart_one {side} stock {symbol}:', response.status_code)
        # print(f'Nội dung phản hồi trade_stock_smart_one {side} stock {symbol}:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print(f'Đã xảy ra lỗi khi gửi yêu cầu trade_stock_smart_one {symbol}:', e)
        return None
    

def buy_stock_smart_one(user_account: str, trade_account: str, url: str, symbol: str, session: str,
                        asp_net_session: str, price: float, volume: float, ref_id: str):
    return trade_stock_smart_one(user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id, "B")

def sell_stock_smart_one(user_account: str, trade_account: str, url: str, symbol: str, session: str, asp_net_session: str, price: float, volume: float, ref_id: str):
    return trade_stock_smart_one(user_account, trade_account, url, symbol, session, asp_net_session, price, volume, ref_id, "S")


def update_order_smart_one(user_account: str, trade_account: str, url: str, symbol: str, session: str, asp_net_session: str, order_num: int, price: float, update_price: float, update_volume: int, ref_id: str, side: str):
    str_order_num = str(order_num)
    str_price = str(price)
    str_update_price = str(update_price)

    payload = json.dumps({
        "group": "O",
        "user": user_account,
        "session": session,
        "language": "vi",
        "extInfo": "1167763841|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "data": {
            "type": "string",
            "cmd": "Web.changeOrder",
            "account": trade_account, 
            "orderNo": str_order_num,
            "refId": ref_id,
            "fisID": "",
            "orderType": "1", #cần chỉnh lại
            "pin": "",
            "nvol": update_volume,
            "nprice": str_update_price,
            "advance": "",
            "price": str_price, 
            "volume": update_volume,
            "symbol": symbol,
            "side": side
        }
    })
    # print(f'check payload to update {symbol} ', payload)

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        # print(f'Mã trạng thái phản hồi update {symbol} :', response.status_code)
        # print(f'Nội dung phản hồi update {symbol}:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu:', e)
        return None




def cancel_order_smart_one(user_account: str, url: str, session: str, asp_net_session: str, order_num: int, ref_id: str, order_type="1"):
    str_order_num = str(order_num)

    payload = json.dumps({
        "group": "O",
        "user": user_account,
        "session": session,  
        "language": "vi", 
        "extInfo": "1167763841|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",  # Adjust extInfo if necessary
        "data": {
            "cmd": "Web.cancelOrder", 
            "orderNo": str_order_num, 
            "refId": ref_id, 
            "fisID": "", 
            "orderType": order_type, 
            "pin": "" 
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }

    # response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        print(f'Mã trạng thái phản hồi cancel_order_smart_one :', response.status_code)
        print(f'Nội dung phản hồi cancel_order_smart_one:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu cancel_order_smart_one:', e)
        return None


def get_orders_status(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str, type: str):
    payload = json.dumps({
        "group": "Q",
        "user": user_account,
        "session": session,
        "data": {
            "type": "string",
            "cmd": "Web.Order.FullAllOrder",
            "p1": "1",  # Trang bắt đầu
            "p2": "9999",  # Số lượng bản ghi cần lấy
            "p3": f"{trade_account},ALL,ALL",  
            "p4": type
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }
    # response = requests.post(url, headers=headers, data=payload)
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=5)
        # print('Mã trạng thái phản hồi get_orders_status:', response.status_code)
        # print('Nội dung phản hồi get_orders_status:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu get_orders_not_matched:', e)
        return None
   

def get_transaction(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str, start_date="26/10/2024", end_date="27/11/2024"):
    payload = json.dumps({
        "group": "B",
        "user": user_account,
        "session": session,
        "data": {
            "type": "cursor",
            "cmd": "ListOrder",
            "p1": trade_account,
            "p2": "",
            "p3": start_date,
            "p4": end_date,
            "p5": "",
            "p6": "",
            "p7": "1",
            "p8": "100",
            "p9": ""
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }

    # response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        # print('Mã trạng thái phản hồi get_transaction:', response.status_code)
        # print('Nội dung phản hồi get_transaction:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu get_transaction:', e)
        return None   




def get_cash_balance(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str,):
    payload = json.dumps({
        "group": "Q",
        "user": user_account,
        "session": session,
        "data": {
            "type": "string",
            "cmd": "Web.Portfolio.AccountStatus",
            "p1": trade_account,
            "p2": "",
            "p3": "",
            "p4": "null"
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }

    # response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        # print('Mã trạng thái phản hồi get_cash_balance:', response.status_code)
        # print('Nội dung phản hồi get_cash_balance:', response.text)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu get_cash_balance:', e)
        return None


def get_stock_balance(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str):
    payload = json.dumps({
        "group": "Q",
        "user": user_account,
        "session": session,
        "data": {
            "type": "string",
            "cmd": "Web.Portfolio.PortfolioStatus",
            "p1": trade_account,
            "p2": "1",
            "p3": "100",
            "p4": ""
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'ASP.NET_SessionId={asp_net_session}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print('Đã xảy ra lỗi khi gửi yêu cầu get_stock_balance:', e)
        return None

# def get_account_status(user_account: str, trade_account: str, url: str, session: str, asp_net_session: str):
#     payload = json.dumps({
#         "group": "Q",
#         "user": user_account,
#         "session": session,
#         "data": {
#             "type": "string",
#             "cmd": "Web.Portfolio.AccountStatus",
#             "p1": trade_account,
#             "p2": "",
#             "p3": "",
#             "p4": "null"
#         }
#     })
#     # print('check payload: ', payload)
#     headers = {
#         'Content-Type': 'application/json',
#         'Cookie': f'ASP.NET_SessionId={asp_net_session}'
#     }

#     try:
#         response = requests.post(url, headers=headers, data=payload, timeout=10)
#         return response
#     except requests.exceptions.RequestException as e:
#         print('Đã xảy ra lỗi khi gửi yêu cầu get_account_status:', e)
#         return None



import json
import re
import time
import logging
import requests

logger = logging.getLogger(__name__)


def get_account_status(
    user_account: str,
    trade_account: str,
    url: str,
    session: str,
    asp_net_session: str
):
    print("\n========== Thông tin gửi lên==========")
    print(f"user_account: {user_account}")
    print(f"trade_account: {trade_account}")
    print(f"session: {session}")
    print(f"asp_net_session: {asp_net_session}")
    payload = {
        "group": "Q",
        "user": user_account,
        "session": session,
        "data": {
            "type": "string",
            "cmd": "Web.Portfolio.AccountStatus",
            "p1": trade_account,
            "p2": "",
            "p3": "",
            "p4": "null"
        }
    }
        logger.info(
        "AccountStatus request: url=%s, cmd=%s, group=%s, "
        "user=%s, trade_account=%s",
        url,
        payload["data"]["cmd"],
        payload["group"],
        user_account,
        trade_account,
    )
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"ASP.NET_SessionId={asp_net_session}",
        "Accept": "application/json, text/plain, */*",
    }

    start_time = time.perf_counter()

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        elapsed = time.perf_counter() - start_time
        response_text = response.text or ""
        content_type = response.headers.get("Content-Type", "")

        # Tìm Incident ID nếu máy chủ trả trang HTML lỗi
        match = re.search(
            r"incident ID is:\s*([0-9]+)",
            response_text,
            re.IGNORECASE
        )
        incident_id = match.group(1) if match else None

        print("\n========== GET ACCOUNT STATUS ==========")
        print(f"HTTP Status : {response.status_code}")
        print(f"Request URL : {response.url}")
        print(f"HTTP Reason : {response.reason}")
        print(f"Elapsed     : {elapsed:.3f} seconds")
        print(f"Content-Type: {content_type}")
        print(f"Encoding    : {response.encoding}")
        print(f"Body length : {len(response.content)} bytes")
        print(f"Incident ID : {incident_id or 'Không tìm thấy'}")

        # In headers phản hồi, che các thông tin nhạy cảm nếu có
        safe_headers = dict(response.headers)
        for key in list(safe_headers):
            if key.lower() in ("set-cookie", "authorization"):
                safe_headers[key] = "[REDACTED]"

        print("Response headers:")
        print(json.dumps(
            safe_headers,
            ensure_ascii=False,
            indent=2
        ))

        print("\nResponse body:")
        print(response_text if response_text else "<EMPTY BODY>")

        # Thử parse JSON
        try:
            response_json = response.json()
            print("\nParsed JSON:")
            print(json.dumps(
                response_json,
                ensure_ascii=False,
                indent=2
            ))
        except ValueError:
            print("\nResponse không phải JSON hợp lệ.")

        print("========== END GET ACCOUNT STATUS ==========\n")

        return response

    except requests.exceptions.RequestException as e:
        elapsed = time.perf_counter() - start_time
        logger.exception(
            "Lỗi request get_account_status sau %.3f giây: %s",
            elapsed,
            type(e).__name__
        )
        return None
