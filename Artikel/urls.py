from django.urls import path
from . import views

app_name = 'Artikel'

urlpatterns = [
    path('playgame/', views.play_game_artikel_one, name='play_game_artikel_one'),

    path('multiplaygame/<str:room_id>/', views.play_game_artikel_multi, name='play_game_artikel_multi'),

]
