from django.contrib import admin
from .models import Verb, Praesens, Praeteritum, Perfekt, Futur_I, Konjunktiv_II

# Register your models here.


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'infinitiv', 'english', 'turkish')
    search_fields = ('id', 'level', 'infinitiv', 'english', 'turkish')
    ordering = ('-id',)


@admin.register(Praesens)
class PraesensAdmin(admin.ModelAdmin):
    list_display = ('id', 'verb__infinitiv', 'sie_Sie')
    search_fields = ('id', 'verb__infinitiv', 'sie_Sie')
    ordering = ('-id',)


@admin.register(Praeteritum)
class PraeteritumAdmin(admin.ModelAdmin):
    list_display = ('id', 'verb__infinitiv', 'sie_Sie')
    search_fields = ('id', 'verb__infinitiv', 'sie_Sie')
    ordering = ('-id',)


@admin.register(Perfekt)
class PerfektAdmin(admin.ModelAdmin):
    list_display = ('id', 'verb__infinitiv', 'partizip_ii')
    search_fields = ('id', 'verb__infinitiv', 'partizip_ii')
    ordering = ('-id',)


@admin.register(Futur_I)
class Futur_IAdmin(admin.ModelAdmin):
    list_display = ('id', 'verb__infinitiv', 'sie_Sie')
    search_fields = ('id', 'verb__infinitiv', 'sie_Sie')
    ordering = ('-id',)


@admin.register(Konjunktiv_II)
class Konjunktiv_IIAdmin(admin.ModelAdmin):
    list_display = ('id', 'verb__infinitiv', 'sie_Sie')
    search_fields = ('id', 'verb__infinitiv', 'sie_Sie')
    ordering = ('-id',)
