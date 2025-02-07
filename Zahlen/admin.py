from django.contrib import admin
from .models import Zahlen

# Register your models here.

@admin.register(Zahlen)
class ZahlenAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'german')
    search_fields = ('id', 'number', 'german')
    ordering = ('-id',)
