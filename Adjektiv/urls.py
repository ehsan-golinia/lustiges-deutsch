from django.urls import path
from . import views

app_name = 'Adjektiv'

urlpatterns = [
    path('playgame/', views.play_game_adjektiv_one, name='play_game_adjektiv_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_adjektiv_multi, name='play_game_adjektiv_multi'),
    path('add/', views.add_adjektiv, name='add_adjektiv'),

]
