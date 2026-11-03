import json
import sys
sys.path.append('e:\\ANguyenBot\\stock-predict-cms-be')
import login_vps

# Retrieve constants from module
user = login_vps.USERNAME
pwd = login_vps.PASSWORD_HASH
device_new = login_vps.RAW_DEVICE_NEW

try:
    # Step 1: attempt login via new API (no handshake needed)
    result = login_vps.login_new(user, pwd, device_new)
    print('Login new API result:')
    print(json.dumps(result, indent=2, ensure_ascii=True))

    if result.get('rc') == 0:
        print('✅ Login successful – no OTP required.')
    else:
                # OTP required – use provided OTP argument or ask for code
        otp_arg = None
        if len(sys.argv) > 1:
            otp_arg = sys.argv[1]
        if otp_arg:
            otp = otp_arg.strip()
        else:
            otp = input('Nhap ma OTP: ').strip()
        # Extract sessionId (sid) from login_new result if present
        session_id = None
        if isinstance(result.get('data'), dict):
            session_id = result['data'].get('sid')
        # Build minimal handshake data for OTP request, including sessionId and ticketId
        otp_handshake = {
            'deviceNew': device_new,
            'deviceInfo': login_vps.DEVICE_INFO_DICT,
            'sessionId': session_id,
            'ticketId': result['data'].get('ticketId') if isinstance(result.get('data'), dict) else None,
        }
        otp_res = login_vps.login_otp(otp_handshake, otp)
        print('OTP result:')
        print(json.dumps(otp_res, indent=2, ensure_ascii=True))
except Exception as e:
    print('Error during login flow:', e)
    raise
