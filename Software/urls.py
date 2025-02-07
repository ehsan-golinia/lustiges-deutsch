from django.urls import path
from . import views

app_name = 'Software'

urlpatterns = [
    path('playgame/', views.play_game_software_one, name='play_game_software_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_software_multi, name='play_game_software_multi'),

]
