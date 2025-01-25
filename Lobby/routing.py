from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chatroom_name>\w+)/$", consumers.YourConsumer.as_asgi()),
    re_path(r"ws/(?P<game_name>\w+)/(?P<gameroom_id>\w+)/$", consumers.GameRoomConsumer.as_asgi()),
    # path('ws/<game_name>/<gameroom_id>/$', consumers.GameRoomConsumer.as_asgi()),
    # path('ws/gameroom/<gameroom_name>', consumers.GameRoomConsumer.as_asgi()),
]
