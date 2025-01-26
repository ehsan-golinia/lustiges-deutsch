from django.urls import path
from . import views

app_name = 'Singular_Plural'

urlpatterns = [
    path('playgame/', views.play_game_singular_plural, name='play_game_singular_plural'),
    path('multiplaygame/<str:room_id>/', views.play_game_singular_plural_multi, name='play_game_singular_plural_multi'),
]
