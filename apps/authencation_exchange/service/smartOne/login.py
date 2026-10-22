from bs4 import BeautifulSoup
import time
import re
import json
import subprocess
import requests

from apps.authencation_exchange.service.http_client import CustomHTTPClient
from apps.authencation_exchange.service.enums import LoginStatusEnum
from apps import api

def login_smart_one_vps_step_1(client, request_verification_token, account, password, cookie):
    payload = {
        "__RequestVerificationToken": request_verification_token,
        "Step": 0,
        "CountLoginFail": 0,
        "AuthenType": None,
        "SessionId": None,
        "Account": account,
        "Password": password,
        "Timeout": 180,
        "Captcha": "Blank"
    }
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'DefaultAccount={account}; _fbp=fb.2.1704153092342.382624434; listStockId=34a41dc6e8eb4ed3836a157b35b388ff; listStockName=VNInDEX; listStock=BDG; _ga=GA1.1.1594567176.1700707680; _ga_EF90CDRSYZ=GS1.1.1711336414.2.1.1711336430.44.0.0; {cookie}; DefaultAccount={account}; startPs=06-07-2020; endPs=05-07-2020; _ga_4WDBKERLGC=GS1.1.1712061855.92.1.1712061896.0.0.0',
        'Origin': 'https://smartone.vps.com.vn',
        'Referer': 'https://smartone.vps.com.vn/Account/Login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
        
    data =  client.post_request_html("/vi-VN/Account/Login", payload=payload, headers=headers)
        
    return data

# def login_smart_one_vps_step_1(request_verification_token, account, password, cookie):
#     curl_command = f'''
#         curl 'https://smartone.vps.com.vn/Account/Login' \
#         -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
#         -H 'Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7' \
#         -H 'Cache-Control: max-age=0' \
#         -H 'Connection: keep-alive' \
#         -H 'Content-Type: application/x-www-form-urlencoded' \
#         -H 'Cookie: DefaultAccount={account}; _fbp=fb.2.1704153092342.382624434; listStockId=34a41dc6e8eb4ed3836a157b35b388ff; listStockName=VNInDEX; listStock=BDG; _ga=GA1.1.1594567176.1700707680; _ga_EF90CDRSYZ=GS1.1.1711336414.2.1.1711336430.44.0.0; {cookie}; DefaultAccount={account}; startPs=06-07-2020; endPs=05-07-2020; _ga_4WDBKERLGC=GS1.1.1712061855.92.1.1712062731.0.0.0' \
#         -H 'Origin: https://smartone.vps.com.vn' \
#         -H 'Referer: https://smartone.vps.com.vn/Account/Login' \
#         -H 'Sec-Fetch-Dest: document' \
#         -H 'Sec-Fetch-Mode: navigate' \
#         -H 'Sec-Fetch-Site: same-origin' \
#         -H 'Sec-Fetch-User: ?1' \
#         -H 'Upgrade-Insecure-Requests: 1' \
#         -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
#         -H 'sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
#         -H 'sec-ch-ua-mobile: ?0' \
#         -H 'sec-ch-ua-platform: "macOS"' \
#         --data-raw '__RequestVerificationToken={request_verification_token}&Step=0&CountLoginFail=0&AuthenType=&SessionId=&Account={account}&Password={password}&Timeout=180&Captcha=Blank'
#   '''
  
#     # with open("curl_step_1.txt", "w") as w:
#     #     w.write(curl_command)
  
#     try:
#             # Run the command and capture the output
#             output = subprocess.check_output(curl_command, shell=True)
#             # Process the output as needed
#             return output
#     except subprocess.CalledProcessError as e:
#             # Handle errors
#             return ""
# def login_get_session_vps_step_2(user_account, password, otp):
#         url = api.LOGIN_URL
#         payload = {
#             "user": user_account,
#             "pass": password,
#             "channel": "I",
#             "language": "vi",
#             "cmd": "Web.sCheckLoginOTP",
#             "p5": otp,
#             "p6": '',
#             "p7": 0,
#             "deviceNew": "xsUpL/sq1XLkHe62VR10KJ1y2TABxBTRAJJPFNGKhc7jU7WadOUla9c4I51 KKeGmXdUojkuDmEUIoi5/wjdb5hH1aUuKzgDfOLPCSVMzwfGXajiYmXETFO4cmPV833B/vnM9PNMMhN4XfKwfJv 1JvZyDdRO0x4e0vaPr4ua Ryc4F BcDsjR1y2D0WzlnZQtLJ53hQcwiwJFHke9gvVF8vICNvrUjSOTPezYpNukS0lLWyJvyH3To=",
#             "deviceName": "Chrome Windows 10",
#             "deviceInfo": "eyJ0eXBlIjoid2ViIiwic291cmNlIjoiUHJpY2Vib2FyZCIsInZlcnNpb24iOiIxLjguMCIsIm1vZGVsIjoiQ2hyb21lIFdpbmRvd3MgMTAiLCJkZXZpY2VPUyI6IiIsImdlb0xvY2F0aW9uIjoiIn0="

#         }

#         headers = {
#             'Content-Type': 'application/json'
#         }

#         try:
#             response = requests.request("POST", url, headers=headers, data=payload)
#             print(f'Mã trạng thái phản hồi login_get_session_vps_step_2 :', response.status_code)
#             print(f'Nội dung phản hồi login_get_session_vps_step_2:', response.text)
#             res_text = response.text
#             res_object = json.loads(res_text)
#             session_id  = res_object['data']['sid']
#             print('check session_id 2: ', session_id)
#             return session_id
#         except requests.exceptions.RequestException as e:
#             print('Đã xảy ra lỗi khi gửi yêu cầu:', e)
#             return None


import json
import logging
import re
import time

import requests

logger = logging.getLogger(__name__)

# Dùng chung cho cả hai bước đăng nhập.
LOGIN_TIMEOUT = 30

DEVICE_INFO = (
    "eyJ0eXBlIjoid2ViIiwic291cmNlIjoiUHJpY2Vib2FyZCIs"
    "InZlcnNpb24iOiIxLjguMCIsIm1vZGVsIjoiQ2hyb21lIFdpbmRvd3MgMTAiLC"
    "JkZXZpY2VPUyI6IiIsImdlb0xvY2F0aW9uIjoiIn0="
)

# Dùng nguyên chuỗi deviceNew đã cung cấp ở bước 1.
# Xác nhận lại với giá trị gốc của hệ thống nếu cần.
DEVICE_NEW = (
    "AcF7KtmYIxmfYQ9q0k7VWsdOEIx/LSV0NewvJmXZwpIOgpdqrvbs7yr2jzVDt7seFcpg1PTi4SFHMDbjETAdIEx7aaMfJeFOzF6axtIKhJVCyjx1Tiz4qSgNUcgL3vzOoHy9w/BBO62VzMhKftk6sD2ctWEjBbS7YMF9OWXdzM6GKm3BD8AI6B/qfOL4kPfcQpWJxR3aTu9bH/Tjw4RLMuGMq8hzZBEFc6bqKg3QIAXflnwkOpU="
)




import re
import time
import requests


def _vps_login_request(step, payload):
    """Gửi request VPS và phân loại phản hồi an toàn."""

    url = api.LOGIN_URL
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    started = time.monotonic()

    logger.info(
        "[VPS LOGIN][%s] START url=%s cmd=%s",
        step,
        url,
        payload.get("cmd"),
    )

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=LOGIN_TIMEOUT,
        )

    except requests.exceptions.Timeout:
        logger.exception(
            "[VPS LOGIN][%s] TIMEOUT after %.2fs",
            step,
            time.monotonic() - started,
        )
        return None, None

    except requests.exceptions.RequestException as exc:
        # Không log URL chi tiết, request headers hoặc payload.
        logger.error(
            "[VPS LOGIN][%s] REQUEST FAILED type=%s",
            step,
            type(exc).__name__,
        )
        return None, None

    elapsed = time.monotonic() - started
    content_type = response.headers.get("Content-Type", "")
    body = response.text or ""

    # Chẩn đoán chuyển hướng HTTP.
    logger.info(
        "[VPS LOGIN][%s] final_url=%s "
        "redirected=%s history_count=%d",
        step,
        response.url,
        bool(response.history),
        len(response.history),
    )

    # Thông tin phản hồi tổng quát.
    logger.info(
        "[VPS LOGIN][%s] RESPONSE status=%s elapsed=%.2fs "
        "content_type=%r body_length=%d",
        step,
        response.status_code,
        elapsed,
        content_type,
        len(body),
    )

    # Lấy mã sự cố gateway nếu phản hồi có chứa mã này.
    incident_match = re.search(
        r"incident ID is:\s*([A-Za-z0-9_-]+)",
        body,
        flags=re.IGNORECASE,
    )

    if incident_match:
        logger.error(
            "[VPS LOGIN][%s] GATEWAY INCIDENT ID=%s",
            step,
            incident_match.group(1),
        )

    # Phân loại lỗi HTTP.
    if not response.ok:
        logger.error(
            "[VPS LOGIN][%s] HTTP ERROR status=%s",
            step,
            response.status_code,
        )
        return response, None

    # Kiểm tra loại nội dung trước khi parse JSON.
    if "json" not in content_type.lower():
        logger.error(
            "[VPS LOGIN][%s] UNEXPECTED CONTENT TYPE=%r",
            step,
            content_type,
        )
        return response, None

    # Parse JSON.
    try:
        result = response.json()
    except ValueError:
        logger.error(
            "[VPS LOGIN][%s] INVALID JSON",
            step,
        )
        return response, None

    # Kiểm tra kiểu dữ liệu gốc.
    if not isinstance(result, dict):
        logger.error(
            "[VPS LOGIN][%s] UNEXPECTED JSON ROOT TYPE=%s",
            step,
            type(result).__name__,
        )
        return response, None

    # Chỉ log tên trường, không log giá trị nhạy cảm.
    logger.info(
        "[VPS LOGIN][%s] JSON root keys=%s",
        step,
        list(result.keys()),
    )

    data = result.get("data")
    if isinstance(data, dict):
        logger.info(
            "[VPS LOGIN][%s] JSON data keys=%s",
            step,
            list(data.keys()),
        )

    logger.info(
        "[VPS LOGIN][%s] RESPONSE PARSED SUCCESSFULLY",
        step,
    )

    return response, result




def _extract_session_id(step, response, result):
    """Lấy session ID nếu phản hồi đúng cấu trúc."""
    if response is None:
        logger.error("[VPS LOGIN][%s] No HTTP response", step)
        return None

    if result is None:
        logger.error(
            "[VPS LOGIN][%s] Cannot extract session: "
            "response was not valid/accepted JSON",
            step,
        )
        return None

    data = result.get("data")
    if not isinstance(data, dict):
        logger.error(
            "[VPS LOGIN][%s] Missing or invalid 'data' field",
            step,
        )
        return None

    session_id = data.get("sid")
    if not session_id:
        # Log trạng thái và các trường an toàn, không log giá trị.
        logger.error(
            "[VPS LOGIN][%s] Missing data.sid; data keys=%s",
            step,
            list(data.keys()),
        )
        return None

    logger.info("[VPS LOGIN][%s] Session ID received successfully", step)
    return session_id


def login_get_session_vps_step_1(user_account, password):
    """Bước 1: kiểm tra tài khoản và mật khẩu."""
    payload = {
        "user": user_account,
        "pass": password,
        "channel": "I",
        "language": "vi",
        "cmd": "Web.sCheckLogin",
        "p5": "",
        "p6": "",
        "p7": 1,
        "deviceNew": DEVICE_NEW,
        "deviceName": "Chrome Windows 10",
        "deviceInfo": DEVICE_INFO,
    }

    logger.info("[VPS LOGIN][STEP 1] Checking credentials")

    response, result = _vps_login_request("STEP 1", payload)

    session_id = _extract_session_id("STEP 1", response, result)

    if not session_id:
        logger.error("[VPS LOGIN][STEP 1] FAILED")
        return None

    logger.info("[VPS LOGIN][STEP 1] SUCCESS")
    return session_id


def login_get_session_vps_step_2(user_account, password, otp):
    """Bước 2: xác thực OTP."""
    payload = {
        "user": user_account,
        "pass": password,
        "channel": "I",
        "language": "vi",
        "cmd": "Web.sCheckLoginOTP",
        "p5": otp,
        "p6": "",
        "p7": 0,
        "deviceNew": DEVICE_NEW,
        "deviceName": "Chrome Windows 10",
        "deviceInfo": DEVICE_INFO,
    }

    logger.info("[VPS LOGIN][STEP 2] Submitting OTP")

    response, result = _vps_login_request("STEP 2", payload)

    session_id = _extract_session_id("STEP 2", response, result)

    if not session_id:
        logger.error("[VPS LOGIN][STEP 2] FAILED")
        return None

    logger.info("[VPS LOGIN][STEP 2] SUCCESS")
    return session_id



def login_smart_one_vps_step_otp(client, request_verification_token, account, password, otp, session_id, cookie):
    otp_payload = {
            "__RequestVerificationToken": request_verification_token,
            "Step": 1,
            "CountLoginFail": 0,
            "AuthenType": "M",
            "SessionId": session_id,
            "Account": account,
            "Password": password,
            "Timeout": 180,
            "Captcha": "Blank",
            "OTP": otp
        }
        
    headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie
        }
        
    return client.post_request_html("/vi-VN/Account/Login", payload=otp_payload, headers=headers)

def login_smart_one_vps_step_otp(request_verification_token, account, password, otp, session_id, cookie):
    curl_command = f'''
    curl 'https://smartone.vps.com.vn/Account/Login' \
        -H 'Accept: application/json, text/javascript, */*; q=0.01' \
        -H 'Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7' \
        -H 'Connection: keep-alive' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -H 'Cookie: DefaultAccount={account}; _fbp=fb.2.1704153092342.382624434; listStockId=34a41dc6e8eb4ed3836a157b35b388ff; listStockName=VNInDEX; listStock=BDG; _ga=GA1.1.1594567176.1700707680; _ga_EF90CDRSYZ=GS1.1.1711336414.2.1.1711336430.44.0.0; {cookie}; DefaultAccount={account}; startPs=06-07-2020; endPs=05-07-2020; _ga_4WDBKERLGC=GS1.1.1712494348.93.1.1712495618.0.0.0' \
        -H 'Origin: https://smartone.vps.com.vn' \
        -H 'Referer: https://smartone.vps.com.vn/vi-VN/Account/Login' \
        -H 'Sec-Fetch-Dest: empty' \
        -H 'Sec-Fetch-Mode: cors' \
        -H 'Sec-Fetch-Site: same-origin' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
        -H 'X-Requested-With: XMLHttpRequest' \
        -H 'sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "macOS"' \
          --data-raw '__RequestVerificationToken={request_verification_token}&Step=1&CountLoginFail=0&AuthenType=M&SessionId={session_id}&Account={account}&Password={password}&Timeout=180&Captcha=Blank&OTP={otp}'
    '''
    # with open("curl_otp.txt", "w") as w:
    #     w.write(curl_command)
    
    try:
            # Run the command and capture the output
            output = subprocess.check_output(curl_command, shell=True)
            # Process the output as needed
            return output
    except subprocess.CalledProcessError as e:
            # Handle errors
            return ""

def get_smart_one_vps_home_page(request_verification_token, account, session_id, cookie):
    curl_command = f'''
            curl 'https://smartone.vps.com.vn/' \
                -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
                -H 'Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7' \
                -H 'Connection: keep-alive' \
                -H 'Cookie: DefaultAccount={account}; _fbp=fb.2.1704153092342.382624434; listStockId=34a41dc6e8eb4ed3836a157b35b388ff; listStockName=VNInDEX; listStock=BDG; _ga=GA1.1.1594567176.1700707680; _ga_EF90CDRSYZ=GS1.1.1711336414.2.1.1711336430.44.0.0; {cookie}; DefaultAccount={account}; startPs=06-07-2020; endPs=05-07-2020; _ga_4WDBKERLGC=GS1.1.1712061855.92.1.1712062731.0.0.0' \
                -H 'Referer: https://smartone.vps.com.vn/Account/Login' \
                -H 'Sec-Fetch-Dest: document' \
                -H 'Sec-Fetch-Mode: navigate' \
                -H 'Sec-Fetch-Site: same-origin' \
                -H 'Sec-Fetch-User: ?1' \
                -H 'Upgrade-Insecure-Requests: 1' \
                -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
                -H 'sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
                -H 'sec-ch-ua-mobile: ?0' \
                -H 'sec-ch-ua-platform: "macOS"'
            '''
            
    # with open("curl_home_page.txt", "w") as w:
    #     w.write(curl_command)
            
    try:
        # Run the command and capture the output
        output = subprocess.check_output(curl_command, shell=True)
        # Process the output as needed
        return output
    except subprocess.CalledProcessError as e:
        # Handle errors
        return ""

def extract_session_id_step_1(html):
    # Parse the HTML string
    if html == "":
        return LoginStatusEnum.FAILED_PASSWORD , ""
        
    # Find the input tag with id "txtSessionId"
    pattern = r'<input[^>]*?id="txtSessionId"[^>]*?/>'
    matches = re.findall(pattern, str(html))
    
    if len(matches) >= 1:
    # Extract the value from the second match
        match_str = matches[0]
        # Extract the value inside the Value attribute using another regular expression
        value_pattern = r'Value="(.*?)"'
        value_match = re.search(value_pattern, match_str)
        if value_match:
            # Extracted value
            extracted_value = value_match.group(1)
            return LoginStatusEnum.BY_PASS_PASSWORD , extracted_value
    return LoginStatusEnum.FAILED_PASSWORD, ""

def extract_session_id_step_2(html):
    if html == "":
        return LoginStatusEnum.FAILED_OTP, "" 
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the script tag containing the JSON-like object
    script_tag = soup.find('script', string=re.compile('var global'))

    if script_tag:
        # Extract the content of the script tag
        script_content = script_tag.string
            # Extract the JSON-like object from the script content
        match = re.search(r'var\s+global\s*=\s*({.*?})', script_content, re.DOTALL)        
        if match:
            json_string = match.group(1) + "\n}"
            json_string = re.sub(r"([a-zA-Z0-9_]+)\s*:", r'"\1":', json_string)
            json_string = '\n'.join([line for line in json_string.split('\n') if '"version":' not in line])
            # Load the JSON string
            global_dict = json.loads(json_string)
            # Get the value of the "session" key
            session_value = global_dict.get("session")
            return LoginStatusEnum.BY_PASS_OTP , session_value
        else:
            return LoginStatusEnum.FAILED_OTP, ""
    else:
        return LoginStatusEnum.FAILED_OTP, ""
    
def login_smartone_vps(request_verification_token, account, password, otp, cookie):
    # Make requests using the HTTP client
    html_step_default = login_smart_one_vps_step_1(request_verification_token, account, password,cookie)
    status_password_step,session_id = extract_session_id_step_1(html=html_step_default)
    
    if status_password_step == LoginStatusEnum.BY_PASS_PASSWORD:
        time.sleep(2)
        html_otp = login_smart_one_vps_step_otp(request_verification_token, account, password, otp, session_id, cookie)
        otp_res_json = json.loads(html_otp)
        success = otp_res_json.get("success")
        message = otp_res_json.get("message")
        
        if success == False:
            return LoginStatusEnum.FAILED_OTP, "", message
        elif success == True:            
            html_after_login = get_smart_one_vps_home_page(request_verification_token, account, session_id, cookie)
            
            parse_status, session = extract_session_id_step_2(html=html_after_login)
            
            if parse_status == LoginStatusEnum.FAILED_OTP:
                return LoginStatusEnum.FAILED_OTP, "", ""
            
            return LoginStatusEnum.BY_PASS_OTP, session, ""
    
    else:
        return LoginStatusEnum.FAILED_PASSWORD, "", ""
