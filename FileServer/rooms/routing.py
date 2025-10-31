from django.urls import re_path

from .consumers import roller

websocket_urlpatterns = [
    re_path(r"ws/rooms/(?P<room_name>\w+)/$", roller.RollerConsumer.as_asgi()),
]
