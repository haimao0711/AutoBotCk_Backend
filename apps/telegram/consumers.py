from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TelegramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Bạn có thể thêm logic khi kết nối

    async def disconnect(self, close_code):
        # Logic khi ngắt kết nối (nếu cần)
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        # Xử lý message hoặc gọi hàm sender.py
        await self.send(text_data=json.dumps({
            'response': f"Bạn vừa gửi: {message}"
        }))
