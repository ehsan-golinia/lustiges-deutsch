from django.urls import path
from . import views

app_name = 'KI'

urlpatterns = [
    path('playgame/', views.play_game_ki_one, name='play_game_ki_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_ki_multi, name='play_game_ki_multi'),

]
