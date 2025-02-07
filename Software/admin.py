from django.contrib import admin
from .models import Software
# Register your models here.

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'turkish', 'german')
    search_fields = ('id', 'english', 'turkish', 'german')
    ordering = ('-id',)
