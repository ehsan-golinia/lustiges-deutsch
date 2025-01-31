from django.urls import path, re_path
from Vokabel.consumers import VokabelGameConsumer
from Singular_Plural.consumers import Singular_PluralGameConsumer
from Verb.consumers import VerbGameConsumer
from Artikel.consumers import ArtikelGameConsumer
from Adjektiv.consumers import AdjektivGameConsumer
from Partizip_II.consumers import Partizip_II_GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/vokabel/(?P<gameroom_id>\w+)/$", VokabelGameConsumer.as_asgi()),
    re_path(r"ws/singular_plural/(?P<gameroom_id>\w+)/$", Singular_PluralGameConsumer.as_asgi()),
    re_path(r"ws/artikel/(?P<gameroom_id>\w+)/$", ArtikelGameConsumer.as_asgi()),
    re_path(r"ws/verb/(?P<gameroom_id>\w+)/$", VerbGameConsumer.as_asgi()),
    re_path(r"ws/partizip_II/(?P<gameroom_id>\w+)/$", Partizip_II_GameConsumer.as_asgi()),
    re_path(r"ws/adjektiv/(?P<gameroom_id>\w+)/$", AdjektivGameConsumer.as_asgi()),
]
