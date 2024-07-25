from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from dm.models import Room
import uuid

class DmConsumer(JsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        # 인스턴스 변수는 생성자 내에서 정의
        super().__init__(*args, **kwargs)
        self.group_name = "" # 인스턴스 변수 group_name 추가
        self.client_id = None


    # 웹소켓 클라이언트가 접속을 요청할 때, 호출된다.
    def connect(self):
        # dm/routing.py 내 정의한 주소에서 접속에 따라,
        # /ws/dm/123/dm/ 요청의 경우,
        # self.scope["url_route"]["kwargs"]["player_id"]는 "123"로 설정된다.
        # self.scope["url_route"] 값은? -> {"args" : (), "kwargs" : {"player_id": "123"}}
        player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.group_name = player_id

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        # 클라이언트에서 전송한 client_id를 가져옵니다.
        self.client_id = self.scope['cookies'].get('client_id')
        
        # client_id가 없으면 새로 생성합니다.
        if not self.client_id:
            self.client_id = str(uuid.uuid4())

        # 본 웹소켓 접속을 허용

        self.accept()

    # 웹소켓 클라이언트가 접속을 끊겼을 때, 호출된다.
    def disconnect(self, code):
        # 소속 그룹에서 빠져나와야 한다.
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )
    # 단일 클라이언트로부터 메세지를 받으면 호출
    def receive_json(self, content, **kwargs):
        #user = self.scope['cookies']['ajs_anonymous_id']

        _type = content["type"]

        if _type == "dm.message":
            message = content["message"]
            sender = self.client_id
            is_fan = content["is_fan"]
            is_player = content["is_player"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "dm.message",
                    "message": message,
                    "sender" : sender,
                    "is_fan" : is_fan,
                    "is_player" : is_player,
                }
            )
        else:
            print(f"Invalid message type : ${_type}")

    # 그룹을 통해 type='dm.message' 메세지를 받으면 호출
    def dm_message(self, message_dict):
        if message_dict["is_player"] or message_dict["sender"] == self.client_id:
            self.send_json({
                "type": "dm.message",
                "message": message_dict["message"],
                "sender" : message_dict["sender"],
            })

class PlayerDmConsumer(JsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        # 인스턴스 변수는 생성자 내에서 정의
        super().__init__(*args, **kwargs)
        self.group_name = "" # 인스턴스 변수 group_name 추가
        self.client_id = None


    # 웹소켓 클라이언트가 접속을 요청할 때, 호출된다.
    def connect(self):
        # dm/routing.py 내 정의한 주소에서 접속에 따라,
        # /ws/dm/123/dm/ 요청의 경우,
        # self.scope["url_route"]["kwargs"]["player_id"]는 "123"로 설정된다.
        # self.scope["url_route"] 값은? -> {"args" : (), "kwargs" : {"player_id": "123"}}
        player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.group_name = player_id

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        # 클라이언트에서 전송한 client_id를 가져옵니다.
        self.client_id = self.scope['cookies'].get('client_id')
        
        # client_id가 없으면 새로 생성합니다.
        if not self.client_id:
            self.client_id = str(uuid.uuid4())

        # 본 웹소켓 접속을 허용

        self.accept()

    # 웹소켓 클라이언트가 접속을 끊겼을 때, 호출된다.
    def disconnect(self, code):
        # 소속 그룹에서 빠져나와야 한다.
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )
    # 단일 클라이언트로부터 메세지를 받으면 호출
    def receive_json(self, content, **kwargs):
        #user = self.scope['cookies']['ajs_anonymous_id']

        _type = content["type"]

        if _type == "dm.message":
            message = content["message"]
            sender = self.client_id
            is_player = content["is_player"]
            is_fan = content["is_fan"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "dm.message",
                    "message": message,
                    "sender" : sender,
                    "is_player" : is_player,
                    "is_fan" : is_fan,
                }
            )
        else:
            print(f"Invalid message type : ${_type}")

    # 그룹을 통해 type='dm.message' 메세지를 받으면 호출
    def dm_message(self, message_dict):
        self.send_json({
            "type": "dm.message",
            "message": message_dict["message"],
            "sender" : message_dict["sender"],
        })