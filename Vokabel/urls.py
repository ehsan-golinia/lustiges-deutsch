from django.urls import path
from . import views

app_name = 'Vokabel'

urlpatterns = [
    path('playgame/', views.play_game_vokabel, name='play_game_vokabel'),
    path('add/', views.add_vokabel, name='add_vokabel'),

]
