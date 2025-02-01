from django.contrib import admin
from .models import UserProfile, GamesRecords, UserScores
from Vokabel.models import Vokabel
from Singular_Plural.models import SingularPlural

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_image')  # Specify the fields you want as columns
    search_fields = ('id', 'user')       # Add a search bar for these fields
    ordering = ('-id',)                                    # Order by id


admin.site.register(UserProfile, UserProfileAdmin)


class GamesRecordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game_name', 'score', 'date')  # Specify the fields you want as columns
    search_fields = ('user', 'game_name', 'score')       # Add a search bar for these fields
    ordering = ('-id',)                                    # Order by id


admin.site.register(GamesRecords, GamesRecordsAdmin)


class UserScoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',
                    'vokabel_score',
                    'singular_plural_score',
                    'artikel_score',
                    'verb_score',
                    'adjektiv_score',
                    'partizip_II_score',
                    'satz_score')  # Specify the fields you want as columns
    search_fields = ('user',)       # Add a search bar for these fields
    ordering = ('id',)                                    # Order by id


admin.site.register(UserScores, UserScoresAdmin)


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
