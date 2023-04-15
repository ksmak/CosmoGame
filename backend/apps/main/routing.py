from django.urls import re_path

from .consumers import ProgressConsumer


websocket_urlpatterns = [
    re_path(r"ws/game/user/(?P<username>\w+)/$", ProgressConsumer.as_asgi()),
]
