"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import dm.routing

# settings.py 경로에 맞춰 DJANGO_SETTINGS_MODULE의 환경변수의 디폴트 값을 지정한다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

# 프로토콜 타입별로 서로 다른 ASGI application을 통해 처리토록 한다.
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # 서비스 규모에 따라 http와 websocket을 분리하여 (웹서버와 채팅서버)를 운영하기도 한다.
    # 장고의 urls include와 비슷한 역할 == URLRouter
    # URLRouter는 path리스트를 인자로 받는다.
    "websocket": URLRouter(
        dm.routing.websocket_urlpatterns
    ),

})