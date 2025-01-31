from django.urls import path
from . import views

app_name = 'Verb'

urlpatterns = [
    path('playgame/', views.play_game_verb_one, name='play_game_verb_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_verb_multi, name='play_game_verb_multi'),
    path('add/', views.add_verb, name='add_verb')
]
