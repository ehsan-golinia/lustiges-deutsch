from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GameRoom(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    game_name = models.CharField(max_length=50)  # vokabel, singular_plural, etc.
    max_players = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='waiting')  # waiting, playing, finished
    board_state = models.JSONField(default=dict)
    active_turn = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_turn')
    players = models.ManyToManyField(User, related_name='game_sessions')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.game_name}, {self.status}'

    class Meta:
        verbose_name = "Game Room"
        verbose_name_plural = "Game Rooms"


class PlayerState(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game_room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='player_states')
    color = models.CharField(max_length=20, null=True, blank=True)
    prev_state = models.IntegerField(default=0)
    game_state = models.IntegerField(default=0)
    game_score = models.IntegerField(default=0)
    dice_history = models.JSONField(default=list)  # Store history as a list
    turn = models.BooleanField(default=False)
    jersey = models.CharField(max_length=10, default='0')

    def __str__(self):
        return f'{self.player.username} in room {self.game_room.room_id}'

    class Meta:
        verbose_name = "Player State"
        verbose_name_plural = "Player States"
