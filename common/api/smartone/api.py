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
import uuid
import logging
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlsplit

import requests

logger = logging.getLogger(__name__)

# Bật True để log đầy đủ payload và các header nhạy cảm.
# Chỉ bật trong môi trường debug riêng, tắt sau khi kiểm tra.
DEBUG_VPS_SENSITIVE = True

SENSITIVE_KEYS = {
    "cookie",
    "set-cookie",
    "authorization",
    "proxy-authorization",
    "session",
    "asp_net_sessionid",
    "password",
    "token",
}


def _mask_sensitive_headers(headers):
    """Che các header có thể chứa thông tin xác thực."""
    result = {}

    for key, value in headers.items():
        if key.lower() in SENSITIVE_KEYS:
            result[key] = (
                str(value)
                if DEBUG_VPS_SENSITIVE
                else "[REDACTED]"
            )
        else:
            result[key] = value

    return result


def _mask_payload(payload):
    """Tạo bản payload an toàn để ghi log."""
    if DEBUG_VPS_SENSITIVE:
        return payload

    copied = json.loads(json.dumps(payload, ensure_ascii=False))
    copied["session"] = "[REDACTED]"
    return copied


def _extract_incident_id(text):
    """Tìm Incident ID trong trang HTML lỗi."""
    patterns = [
        r"incident\s+ID\s+is\s*:\s*([0-9]+)",
        r"incident\s+id\s*[:=]\s*([0-9]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def get_account_status(
    user_account: str,
    trade_account: str,
    url: str,
    session: str,
    asp_net_session: str,
):
    request_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc).isoformat()
    start_time = time.perf_counter()

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
            "p4": "null",
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Cookie": f"ASP.NET_SessionId={asp_net_session}",
    }

    print("\n========== VPS ACCOUNT STATUS REQUEST ==========")
    print(f"Request ID       : {request_id}")
    print(f"Started at (UTC) : {started_at}")
    print(f"URL              : {url}")
    print("Method           : POST")
    print(f"User account     : {user_account}")
    print(f"Trade account    : {trade_account}")
    print(f"Command          : {payload['data']['cmd']}")
    print(f"Group            : {payload['group']}")

    print("\nPayload:")
    print(json.dumps(
        _mask_payload(payload),
        ensure_ascii=False,
        indent=2,
    ))

    # Không in cookie/session thô trong log thông thường.
    print("\nInput session diagnostics:")
    print(f"session length   : {len(session) if session else 0}")
    print(
        "session SHA256   : "
        + (
            hashlib.sha256(session.encode()).hexdigest()
            if DEBUG_VPS_SENSITIVE and session
            else "[NOT LOGGED]"
        )
    )
    print(
        f"ASP.NET session length: "
        f"{len(asp_net_session) if asp_net_session else 0}"
    )
    print(
        "ASP.NET session SHA256: "
        + (
            hashlib.sha256(asp_net_session.encode()).hexdigest()
            if DEBUG_VPS_SENSITIVE and asp_net_session
            else "[NOT LOGGED]"
        )
    )

    try:
        # Chuẩn bị request trước khi gửi để kiểm tra chính xác
        # những gì requests đã dựng.
        req = requests.Request(
            method="POST",
            url=url,
            headers=headers,
            json=payload,
        )
        prepared = requests.Session().prepare_request(req)

        print("\nPrepared request:")
        print(f"Method           : {prepared.method}")
        print(f"Prepared URL     : {prepared.url}")
        print(f"Host             : {urlsplit(prepared.url).netloc}")
        print("Prepared headers:")
        print(json.dumps(
            _mask_sensitive_headers(dict(prepared.headers)),
            ensure_ascii=False,
            indent=2,
        ))

        body = prepared.body
        if isinstance(body, bytes):
            body_text = body.decode("utf-8", errors="replace")
        else:
            body_text = body or ""

        print(f"Request body size: {len(body_text.encode('utf-8'))} bytes")
        print(f"Request body SHA256: {hashlib.sha256(body_text.encode('utf-8')).hexdigest()}")

        print("Prepared body:")
        if DEBUG_VPS_SENSITIVE:
            print(body_text)
        else:
            print(json.dumps(
                _mask_payload(payload),
                ensure_ascii=False,
                indent=2,
            ))

        logger.info(
            "[VPS REQUEST] request_id=%s started_at=%s url=%s "
            "method=%s cmd=%s group=%s user=%s trade_account=%s "
            "body_sha256=%s",
            request_id,
            started_at,
            prepared.url,
            prepared.method,
            payload["data"]["cmd"],
            payload["group"],
            user_account,
            trade_account,
            hashlib.sha256(body_text.encode("utf-8")).hexdigest(),
        )

        # Dùng cùng prepared request để tránh khác biệt giữa
        # request được log và request thực sự gửi đi.
        with requests.Session() as client:
            response = client.send(prepared, timeout=10)

        elapsed = time.perf_counter() - start_time
        response_text = response.text or ""
        content_type = response.headers.get("Content-Type", "")
        incident_id = _extract_incident_id(response_text)

        print("\n========== VPS ACCOUNT STATUS RESPONSE ==========")
        print(f"Request ID       : {request_id}")
        print(f"HTTP Status      : {response.status_code}")
        print(f"HTTP Reason      : {response.reason}")
        print(f"Response URL     : {response.url}")
        print(f"Elapsed          : {elapsed:.3f} seconds")
        print(f"Content-Type     : {content_type}")
        print(f"Encoding         : {response.encoding}")
        print(f"Apparent encoding: {response.apparent_encoding}")
        print(f"Body length      : {len(response.content)} bytes")
        print(f"Body SHA256      : {hashlib.sha256(response.content).hexdigest()}")
        print(f"Incident ID      : {incident_id or 'Không tìm thấy'}")

        print("\nResponse headers:")
        print(json.dumps(
            _mask_sensitive_headers(dict(response.headers)),
            ensure_ascii=False,
            indent=2,
        ))

        # Chỉ in response body; nếu API trả dữ liệu nhạy cảm,
        # cần bảo vệ file log và quyền truy cập vào log.
        print("\nResponse body:")
        print(response_text if response_text else "<EMPTY BODY>")

        print("\nJSON parsing:")
        try:
            response_json = response.json()

            print(json.dumps(
                response_json,
                ensure_ascii=False,
                indent=2,
            ))

            print(f"JSON command     : {response_json.get('cmd')}")
            print(f"JSON rc          : {response_json.get('rc')}")
            print(f"JSON rs          : {response_json.get('rs')}")

            if response_json.get("cmd") != payload["data"]["cmd"]:
                print("WARNING: Command trong response không khớp request.")

        except ValueError:
            response_json = None
            print("Response không phải JSON hợp lệ.")

        if "json" not in content_type.lower():
            print(
                "\nWARNING: Server không trả Content-Type JSON. "
                "HTTP 200 không đồng nghĩa API thành công."
            )

        logger.info(
            "[VPS RESPONSE] request_id=%s status=%s elapsed=%.3fs "
            "content_type=%s body_bytes=%s incident_id=%s "
            "body_sha256=%s",
            request_id,
            response.status_code,
            elapsed,
            content_type,
            len(response.content),
            incident_id,
            hashlib.sha256(response.content).hexdigest(),
        )

        print("========== END ACCOUNT STATUS ==========\n")
        return response

    except requests.exceptions.RequestException as exc:
        elapsed = time.perf_counter() - start_time

        logger.exception(
            "[VPS REQUEST ERROR] request_id=%s elapsed=%.3fs "
            "exception_type=%s error=%s",
            request_id,
            elapsed,
            type(exc).__name__,
            str(exc),
        )

        print("\n========== VPS REQUEST ERROR ==========")
        print(f"Request ID : {request_id}")
        print(f"Elapsed    : {elapsed:.3f} seconds")
        print(f"Exception  : {type(exc).__name__}")
        print(f"Error      : {exc}")
        print("=======================================\n")

        return None