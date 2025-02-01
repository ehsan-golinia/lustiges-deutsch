from django.urls import path
from . import views

app_name = 'Satz'

urlpatterns = [
    path('playgame/', views.play_game_satz_one, name='play_game_satz_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_satz_multi, name='play_game_satz_multi'),
]
