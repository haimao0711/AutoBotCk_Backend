import requests
import time
from common.signal.enums import SignalTelegramEnum
from apps.telegram.enum.enums import MessageTypeEnum
from apps.authencation.user.models import User
from apps.telegram.messages import (BUY_FAILED_SIGNAL, BUY_REQUEST_FAILED_SIGNAL, BUY_FAILED_UPDATE, BUY_ORDER_DETAIL, BUY_UPDATE_DETAIL, BUY_CANCEL_DETAIL, BUY_MATCHED_DETAIL,
                                    BUY_ORDER_OVERRAL, BUY_CANCEL_OVERRAL, BUY_UPDATE_OVERRAL, BUY_MATCHED_OVERRAL, BUY_SIGNAL, BUY_REQUEST_SIGNAL,
                                    DEFAULT_MESSAGE, LOGIN_FAILED, LOGIN_SUCCESS, SESSION_FAILED, NOTIFY_LOGIN, NOTIFY_RUNNING,
                                    SELL_FAILED_SIGNAL, SELL_REQUEST_FAILED_SIGNAL, SELL_FAILED_UPDATE, SELL_ORDER_OVERRAL, SELL_UPDATE_OVERRAL, SELL_CANCEL_OVERRAL, SELL_MATCHED_OVERRAL,
                                    SELL_ORDER_DETAIL, SELL_UPDATE_DETAIL, SELL_CANCEL_DETAIL, SELL_MATCHED_DETAIL, SELL_SIGNAL, SELL_REQUEST_SIGNAL, STOPLOSS_SIGNAL, TAKEPROFIT_SIGNAL)
'''
BOT TELEGRAM USED TO TEST
https://t.me/testbotalert
'''
# TELEGRAM_BOT_TOKEN = "7185215713:AAEr2rF8AxohXesTNyV_vqYJgJdRcNUVZMI"
# TELEGRAM_CHANNEL_ID = "-1002249258520"

#Bot Mao
# TELEGRAM_BOT_TOKEN = '7510360148:AAHYGFK1oaJpUXFwsneFNui7jEVR7MzkIBo'
# TELEGRAM_CHANNEL_ID = '7789695074'

#Group Bot A Nguyen
# TELEGRAM_BOT_TOKEN = '7510360148:AAHYGFK1oaJpUXFwsneFNui7jEVR7MzkIBo'
# TELEGRAM_CHANNEL_ID = '-1002305526353'

#Hành động Bot A Nguyen
TELEGRAM_BOT_TOKEN_ATC = '7985837809:AAG8IQT71-LAudSXXqiS3z3dnKLwiFsPeEo'
TELEGRAM_CHANNEL_ID_ATC = '-1002334297234'



#Bot cũ
# TELEGRAM_BOT_TOKEN = '6834862302:AAGc2ShKff8AmfVo44f2TfXlD9qYZAfaycE'
# TELEGRAM_CHANNEL_ID = '-1002026273140'

PLATFROM = 'smartOne'
WEBSITE = 'https://smartone.vps.com.vn'


def define_message(type: SignalTelegramEnum, **kwargs):
    match type:
        case SignalTelegramEnum.NOTIFY_RUNNING.value:
            return NOTIFY_RUNNING.format(**kwargs["kwargs"])

        case SignalTelegramEnum.NOTIFY_LOGIN.value:
            return NOTIFY_LOGIN.format(**kwargs["kwargs"])

        case SignalTelegramEnum.LOGIN_SUCCESS.value:
            return LOGIN_SUCCESS.format(**kwargs["kwargs"])
        case SignalTelegramEnum.LOGIN_FAILED.value:
            return LOGIN_FAILED.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SESSION_FAILED.value:
            return SESSION_FAILED.format(**kwargs["kwargs"])

        case SignalTelegramEnum.BUY_SUCCESS.value:
            return BUY_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_REQUEST_SUCCESS.value:
            return BUY_REQUEST_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_FAILED.value:
            return BUY_FAILED_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_REQUEST_FAILED.value:
            return BUY_REQUEST_FAILED_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_FAILED_UPDATE.value:
            return BUY_FAILED_UPDATE.format(**kwargs["kwargs"])

        case SignalTelegramEnum.BUY_ORDER_DETAIL.value:
            return BUY_ORDER_DETAIL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_UPDATE_DETAIL.value:
            return BUY_UPDATE_DETAIL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_CANCEL_DETAIL.value:
            return BUY_CANCEL_DETAIL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_MATCHED_DETAIL.value:
            return BUY_MATCHED_DETAIL.format(**kwargs["kwargs"])
        
        case SignalTelegramEnum.BUY_ORDER_OVERRAL.value:
            return BUY_ORDER_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_UPDATE_OVERRAL.value:
            return BUY_UPDATE_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_CANCEL_OVERRAL.value:
            return BUY_CANCEL_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.BUY_MATCHED_OVERRAL.value:
            return BUY_MATCHED_OVERRAL.format(**kwargs["kwargs"])

        case SignalTelegramEnum.SELL_SUCCESS.value:
            return SELL_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_REQUEST_SUCCESS.value:
            return SELL_REQUEST_SIGNAL.format(**kwargs["kwargs"])       
        case SignalTelegramEnum.SELL_FAILED.value:
            return SELL_FAILED_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_REQUEST_FAILED.value:
            return SELL_REQUEST_FAILED_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_FAILED_UPDATE.value:
            return SELL_FAILED_UPDATE.format(**kwargs["kwargs"])
              
        case SignalTelegramEnum.SELL_ORDER_OVERRAL.value:
            return SELL_ORDER_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_UPDATE_OVERRAL.value:
            return SELL_UPDATE_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_CANCEL_OVERRAL.value:
            return SELL_CANCEL_OVERRAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_MATCHED_OVERRAL.value:
            return SELL_MATCHED_OVERRAL.format(**kwargs["kwargs"])
        
        case SignalTelegramEnum.SELL_ORDER_DETAIL.value:
            return SELL_ORDER_DETAIL.format(**kwargs["kwargs"]) 
        case SignalTelegramEnum.SELL_UPDATE_DETAIL.value:
            return SELL_UPDATE_DETAIL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_CANCEL_DETAIL.value:
            return SELL_CANCEL_DETAIL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.SELL_MATCHED_DETAIL.value:
            return SELL_MATCHED_DETAIL.format(**kwargs["kwargs"])

        case SignalTelegramEnum.STOPLOSS.value:
            return STOPLOSS_SIGNAL.format(**kwargs["kwargs"])
        case SignalTelegramEnum.TAKEPROFIT.value:
            return TAKEPROFIT_SIGNAL.format(**kwargs["kwargs"])

        case _:
            return DEFAULT_MESSAGE



# def send_message_telegram(user: User, message_type: MessageTypeEnum, message: str, timeout_per_request=3, max_duration=15) -> None:
            
#     # webhook_url = 'https://discord.com/api/webhooks/1377123602570285147/Z1A-20yyLW5HLeXGcC3MUDYPWv8_uDv_Sd59A-l8C1h0DBGRPzeYPyqzxtAndnpJ-9LQ'
#     webhook_url = user.telegram_bot_token
#     if message_type == MessageTypeEnum.ACT:
#         if not user.telegram_bot_token_atc or not user.telegram_channel_id_atc:
#             print("❌ Thiếu token hoặc channel ID ATC — không gửi tin nhắn.")
#             return  # Thoát nếu thiếu thông tin
        
#         # webhook_url = 'https://discord.com/api/webhooks/1377464762421481542/llZDUX33gS1lDHyUYlvOaILDvrTbwRo3Tt7HtvCbHsye3VN4wnOaO19m4VEnQJ5jEqrh'
#         webhook_url = user.telegram_bot_token_atc

#     json_data = {
#         "content": message
#     }

#     start_time = time.time()

#     while time.time() - start_time < max_duration:
#         try:
#             response = requests.post(url=webhook_url, json=json_data, timeout=timeout_per_request)

#             if response.status_code in (200, 204):
#                 print("📩 Gửi tin nhắn Discord thành công!")
#                 return
            
#             print(f"⚠️ Lỗi HTTP {response.status_code}: {response.text}")

#         except requests.RequestException as error:
#             print(f"🚨 Lỗi mạng: {error}")

#         if time.time() - start_time + 2 < max_duration:
#             print("🔄 Thử lại sau 2 giây...")
#             time.sleep(2)
#         else:
#             break

#     print("❌ Hết thời gian! Bỏ qua tin nhắn.")

def send_message_telegram(
    user: User,
    message_type: MessageTypeEnum,
    message: str,
    timeout_per_request=3,
    max_duration=10
) -> None:
    """
    Gửi tin nhắn Telegram với retry trong vòng tối đa 10 giây.
    - Nếu lỗi mạng hoặc Telegram quá tải -> thử lại cho đến khi hết 10 giây.
    - Nếu hết thời gian mà vẫn lỗi -> bỏ qua, không làm treo luồng chính.
    """
    try:
        # Xác định webhook URL
        webhook_url = user.telegram_bot_token
        if message_type == MessageTypeEnum.ACT:
            if not user.telegram_bot_token_atc or not user.telegram_channel_id_atc:
                print("❌ Thiếu token hoặc channel ID ATC — không gửi tin nhắn.")
                return  # Bỏ qua nếu thiếu dữ liệu
            webhook_url = user.telegram_bot_token_atc

        # Nếu không có webhook_url => thoát sớm
        if not webhook_url:
            print("❌ Không tìm thấy webhook_url — bỏ qua gửi tin nhắn.")
            return

        json_data = {"content": message}

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < max_duration:
            attempt += 1
            try:
                response = requests.post(
                    url=webhook_url,
                    json=json_data,
                    timeout=timeout_per_request
                )

                # Thành công thì dừng ngay
                if response.status_code in (200, 204):
                    print(f"📩 Gửi tin nhắn Telegram thành công sau {attempt} lần thử!")
                    return

                # Lỗi từ Telegram (ví dụ rate limit)
                print(f"⚠️ Lỗi HTTP {response.status_code}: {response.text}")

            except requests.Timeout:
                print(f"⏳ Timeout lần {attempt}.")
            except requests.RequestException as error:
                print(f"🚨 Lỗi mạng hoặc kết nối lần {attempt}: {error}")

            # Đợi 2 giây trước khi thử lại, nhưng không vượt quá max_duration
            if time.time() - start_time + 2 >= max_duration:
                break
            print("🔄 Đợi 2 giây trước khi thử lại...")
            time.sleep(2)

        print("❌ Hết 10 giây mà chưa gửi được tin nhắn, bỏ qua.")

    except Exception as e:
        # Bắt mọi lỗi bất ngờ, không cho treo luồng chính
        print(f"[Error] send_message_telegram gặp lỗi nghiêm trọng: {e}")

def send_message(user: User, message_type: MessageTypeEnum, type: SignalTelegramEnum, **kwargs):
    message = define_message(type, kwargs=kwargs)
    send_message_telegram(user=user, message_type=message_type, message=message)
