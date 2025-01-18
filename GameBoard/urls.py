from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'GameBoard'

urlpatterns = [
    path('vokabel', views.play_game_vokabel, name='play_game_vokabel'),
]
