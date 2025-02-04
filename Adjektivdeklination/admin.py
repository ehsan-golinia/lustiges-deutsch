from django.contrib import admin
from .models import Adjektivdeklination, AdjKasus
# Register your models here.


@admin.register(Adjektivdeklination)
class AdjektivdeklinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'turkish', 'type')
    search_fields = ('id', 'english', 'turkish', 'type')
    ordering = ('-id',)


@admin.register(AdjKasus)
class AdjKasusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'akk', 'dat', 'gen')
    search_fields = ('id', 'nom', 'akk', 'dat', 'gen')
    ordering = ('-id',)

