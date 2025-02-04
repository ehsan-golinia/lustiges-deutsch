from django.urls import path
from . import views

app_name = 'Adjektivdeklination'

urlpatterns = [
    path('playgame/', views.play_game_adjektivdeklination_one, name='play_game_adjektivdeklination_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_adjektivdeklination_multi, name='play_game_adjektivdeklination_multi'),
    path('add/', views.add_adjektivdeklination, name='add_adjektivdeklination'),
]
