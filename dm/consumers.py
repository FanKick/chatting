from channels.generic.websocket import WebsocketConsumer
import json

# 장고 view함수와 유사한 역할, 
class DmConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
    # 웹소켓 클라이언트에서 text frame으로 보내면, text_data 담기고
    # binary data frame으로 보내면 bytes_data 인자에 값이 담겨 호출된다.
    def receive(self, text_data=None, bytes_data=None):
        obj = json.loads(text_data)

        json_string: str = json.dumps(obj)
        self.send(json_string)
        