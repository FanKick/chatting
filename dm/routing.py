from django.urls import path
from dm.consumers import DmConsumer

# 장고의 urls patterns와 유사한 역할
# 장고 기본 urls.py urlpatterns와 다르게
# 장고에서 찾아서 읽어가는게 아니라, 우리가 직접 asgi.py 임포트하기 때문에
# websocket_urlpatterns 이름말고 다른 이름이어도 상관없다.

websocket_urlpatterns = [
    path('ws/dm/', DmConsumer.as_asgi()),
]