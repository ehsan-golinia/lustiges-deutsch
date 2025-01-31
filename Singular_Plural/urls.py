from django.urls import path
from . import views

app_name = 'Singular_Plural'

urlpatterns = [
    path('playgame/', views.play_game_singular_plural_one, name='play_game_singular_plural_one'),
    path('multiplaygame/<str:room_id>/', views.play_game_singular_plural_multi, name='play_game_singular_plural_multi'),
]
