from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('settings/', views.user_settings, name='user_settings'),
    path('profile/', views.user_profile, name='user_profile'),
]
