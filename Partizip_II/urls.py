from django.urls import path
from . import views

app_name = 'Partizip_II'

urlpatterns = [
    path('playgame/', views.play_game_partizip_II_one, name='play_game_partizip_II_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_partizip_II_multi, name='play_game_partizip_II_multi'),
]
