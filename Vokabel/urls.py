from django.urls import path
from . import views

app_name = 'Vokabel'

urlpatterns = [
    path('playgame/', views.play_game_vokabel, name='play_game_vokabel'),
    path('multiplaygame/<str:room_id>/', views.play_game_vokabel_multi, name='play_game_vokabel_multi'),
    path('add/', views.add_vokabel, name='add_vokabel'),

]
