from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from dm.models import Room

class DmConsumer(JsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        # 인스턴스 변수는 생성자 내에서 정의
        super().__init__(*args, **kwargs)
        self.group_name = "" # 인스턴스 변수 group_name 추가

    # 웹소켓 클라이언트가 접속을 요청할 때, 호출된다.
    def connect(self):
        # dm/routing.py 내 정의한 주소에서 접속에 따라,
        # /ws/dm/123/dm/ 요청의 경우,
        # self.scope["url_route"]["kwargs"]["room_pk"]는 "123"로 설정된다.
        # self.scope["url_route"] 값은? -> {"args" : (), "kwargs" : {"room_pk": "123"}}
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        self.group_name = Room.make_chat_group_name(room_pk=room_pk)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

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
        _type = content["type"]

        if _type == "dm.message":
            message = content["message"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "dm.message",
                    "message": message,
                }
            )
        else:
            print(f"Invalid message type : ${_type}")

    # 그룹을 통해 type='dm.message' 메세지를 받으면 호출
    def dm_message(self, message_dict):
        self.send_json({
            "type": "dm.message",
            "message": message_dict["message"],
        })