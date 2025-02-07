"""
URL configuration for LustigesDeutsch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static


handler404 = 'LustigesDeutsch.views.custom_page_not_found'


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('accounts.urls')),
    path('lobby/', include('Lobby.urls')),
    path('all_ranking/', views.all_ranking, name='all_ranking'),
    path('<str:game_name>/playervsplayer/', views.playervsplayer),
    path('vokabel/', include('Vokabel.urls')),
    path('singular_plural/', include('Singular_Plural.urls')),
    path('artikel/', include('Artikel.urls')),
    path('verb/', include('Verb.urls')),
    path('partizip_II/', include('Partizip_II.urls')),
    path('adjektiv/', include('Adjektiv.urls')),
    path('satz/', include('Satz.urls')),
    path('adjektivdeklination/', include('Adjektivdeklination.urls')),
    path('zahlen/', include('Zahlen.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
