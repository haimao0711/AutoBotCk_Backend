# apps/stockSocket/services/socket_service.py
import json
import websocket
import threading
from .cache_service import update_price

SOCKET_URL = "wss://price-ws.example.com/realtime"  # placeholder

def on_message(ws, message):
    try:
        data = json.loads(message)
        # ví dụ payload: {"symbol": "VND", "price": 17300}
        symbol = data.get("symbol")
        price = data.get("price")
        if symbol and price:
            update_price(symbol, price)
    except Exception as e:
        print("Error parsing message:", e)

def on_error(ws, error):
    print("Socket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Socket closed")

def on_open(ws):
    # Gửi lệnh subscribe
    payload = {
        "type": "subscribe",
        "symbols": ["VND", "VCB", "SSI"],  # danh sách theo dõi
    }
    ws.send(json.dumps(payload))

def start_socket():
    ws = websocket.WebSocketApp(
        SOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    wst = threading.Thread(target=ws.run_forever, daemon=True)
    wst.start()
