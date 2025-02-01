from django.contrib import admin
from .models import Satz

# Register your models here.

@admin.register(Satz)
class SatzAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'turkish', 'german')
    search_fields = ('english', 'turkish', 'german')
    ordering = ('-id',)
