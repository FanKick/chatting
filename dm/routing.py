# 장고의 urls patterns와 유사한 역할
# 장고 기본 urls.py urlpatterns와 다르게
# 장고에서 찾아서 읽어가는게 아니라, 우리가 직접 asgi.py 임포트하기 때문에
# websocket_urlpatterns 이름말고 다른 이름이어도 상관없다.

from django.urls import path
from dm import consumers

websocket_urlpatterns = [
    path("ws/dm/<str:user_id>/<str:player_id>/dm/", consumers.DmConsumer.as_asgi()),
    path("ws/dm/player/<str:player_id>/", consumers.PlayerDmConsumer.as_asgi()),
]