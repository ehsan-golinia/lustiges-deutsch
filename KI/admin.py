from django.contrib import admin
from .models import KI

# Register your models here.

@admin.register(KI)
class KIAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'turkish', 'german')
    search_fields = ('id', 'english', 'turkish', 'german')
    ordering = ('-id',)