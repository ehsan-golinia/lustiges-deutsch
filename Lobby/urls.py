from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:game_name>/', views.create_room, name='create_room'),
    path('join/<str:room_id>/', views.join_room, name='join_room'),
    path('wait/<str:room_id>/', views.wait_room, name='wait_room'),
    path('check_status/<str:room_id>/', views.check_status, name='check_status'),
    path('cancel/<str:room_id>/', views.cancel_room, name='cancel_room'),
    path('finish/<str:game_name>/<str:room_id>/', views.finish_room, name='finish_room'),
]
