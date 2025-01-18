from django.contrib import admin
from .models import UserProfile, GamesRecords
from GameBoard.models import Vokabel, SingularPlural

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(GamesRecords)


class VokabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'german', 'english', 'turkish')  # Specify the fields you want as columns
    search_fields = ('german', 'english', 'turkish')       # Add a search bar for these fields
    # list_filter = ('german', 'english')                   # Add filtering options if needed
    ordering = ('-id',)                                    # Order by id


admin.site.register(Vokabel, VokabelAdmin)


class SingularPluralAdmin(admin.ModelAdmin):
    list_display = ('id', 'singular', 'plural')  # Specify the fields you want as columns
    search_fields = ('singular', 'plural')       # Add a search bar for these fields
    # list_filter = ('german', 'english')                   # Add filtering options if needed
    ordering = ('-id',)                                    # Order by id descending


admin.site.register(SingularPlural, SingularPluralAdmin)
