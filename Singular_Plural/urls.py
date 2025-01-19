from django.urls import path
from . import views

app_name = 'Singular_Plural'

urlpatterns = [
    path('playgame/', views.play_game_singular_plural, name='play_game_singular_plural'),
]
