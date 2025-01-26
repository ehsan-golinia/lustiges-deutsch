from django.urls import path, re_path
from Vokabel.consumers import VokabelGameConsumer


websocket_urlpatterns = [
    re_path(r"ws/vokabel/(?P<gameroom_id>\w+)/$", VokabelGameConsumer.as_asgi()),
]
