from django.contrib import admin
from .models import GameRoom, PlayerState

# Register your models here.


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'game_name', 'status', 'active_turn', 'get_players', 'winner', 'max_players', 'created_at')
    search_fields = ('room_id', 'game_name', 'status', 'players__username', 'winner__username', 'created_at')
    ordering = ('-created_at',)

    def get_players(self, obj):
        return ", ".join([player.username for player in obj.players.all()])
    get_players.short_description = 'Players'  # Column header in admin


@admin.register(PlayerState)
class PlayerStateAdmin(admin.ModelAdmin):
    list_display = ('player', 'game_room__game_name', 'color', 'jersey', 'game_score', 'turn')
    search_fields = ('player__username', 'game_room__game_name', 'game_room__room_id', 'jersey', 'color', 'turn')
    ordering = ('player__username',)
