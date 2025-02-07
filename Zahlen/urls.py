from django.urls import path
from . import views

app_name = 'Zahlen'

urlpatterns = [
    path('playgame/', views.play_game_zahlen_one, name='play_game_zahlen_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_zahlen_multi, name='play_game_zahlen_multi'),
    path('add/', views.add_zahlen, name='add_zahlen'),
]
