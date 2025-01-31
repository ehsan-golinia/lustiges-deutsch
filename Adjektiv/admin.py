from django.contrib import admin
from .models import Adjektiv

# Register your models here.

@admin.register(Adjektiv)
class AdjektivAdmin(admin.ModelAdmin):
    list_display = ['id', 'english', 'turkish', 'positiv', 'komparativ', 'superlativ']
    search_fields = ['id', 'english', 'turkish', 'positiv', 'komparativ', 'superlativ']
    ordering = ('-id',)
