from django.urls import re_path

from .consumers import markdown

websocket_urlpatterns = [
    re_path(r"ws/file/(?P<file_id>\w+)/$", markdown.FileConsumer.as_asgi()),
]
