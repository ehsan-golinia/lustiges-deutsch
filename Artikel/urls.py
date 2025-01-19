from django.urls import path
from . import views

app_name = 'Artikel'

urlpatterns = [
    path('playgame/', views.play_game_artikel, name='play_game_artikel'),
]
