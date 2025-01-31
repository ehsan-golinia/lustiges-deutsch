from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from Lobby.models import GameRoom, PlayerState
from Verb.models import Verb
from accounts.models import GamesRecords, UserProfile, UserScores
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
import random
from LustigesDeutsch.constants import MIN_SCORE


class VerbGameConsumer(WebsocketConsumer):
    def connect(self):
        self.this_user = self.scope['user']
        self.gameroom_id = self.scope['url_route']['kwargs']['gameroom_id']
        self.game_name = 'verb'
        self.MIN_SCORE = MIN_SCORE
        self.game_room = get_object_or_404(
            GameRoom, room_id=self.gameroom_id, game_name=self.game_name)
        async_to_sync(self.channel_layer.group_add)(
            self.gameroom_id,
            self.channel_name
        )
        self.accept()


        self.first_event = {
            'type': 'first_game_state',
            'board_state': self.game_room.board_state,
            'active_turn': self.game_room.active_turn.username,
            'game_status': self.game_room.status,
            'winner': self.game_room.winner.username if self.game_room.winner else None,
            'players': [
                    {
                        'id': pl.player.id,
                        'first_name': pl.player.first_name,
                        'username': pl.player.username,
                        'profile_image': pl.player.profile.profile_image.url,
                        'prev_state': pl.prev_state,
                        'game_state': pl.game_state,
                        'game_score': pl.game_score,
                        'color': pl.color,
                        'turn': pl.turn,
                        'dice_history': pl.dice_history
                    } for pl in self.game_room.player_states.all()
                ],
        }

        self.send(text_data=json.dumps(self.first_event))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.gameroom_id,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        rand_q = None
        select_type = None
        ended_user = None
        if text_data_json['action'] == 'end_game':
            ended_user = text_data_json['username']
            select_type = 'end_game_state'
            self.game_room.status = 'cancelled'
            self.game_room.save()
        elif text_data_json['action'] == 'roll_dice':
            select_type = 'roll_dice_state'
            dice_value = text_data_json['dice_value']
            self.game_room.board_state['dice_number'] = dice_value
            game_state = self.game_room.player_states.get(turn=True).game_state
            self.game_room.active_turn = self.game_room.player_states.get(turn=True).player

            if game_state + dice_value <= 30:
                dice_history = self.game_room.player_states.get(turn=True).dice_history
                dice_history.append(dice_value)
                self.game_room.player_states.filter(turn=True).update(
                    prev_state=game_state,
                    game_state=dice_value + game_state,
                    dice_history=dice_history)
                self.game_room.save()
                if self.game_room.player_states.get(turn=True).game_state != 30:
                    self.game_room.board_state['q_box'] = True
                    rand_q = self.get_quiz()
            else:
                current_jersey = self.game_room.player_states.get(turn=True).jersey
                if current_jersey == str(self.game_room.max_players):
                    current_jersey = '1'
                else:
                    current_jersey = str(int(current_jersey) + 1)
                self.game_room.player_states.filter(turn=True).update(
                    turn=False
                )
                self.game_room.player_states.filter(jersey=current_jersey).update(
                    turn=True
                )
                self.game_room.active_turn = self.game_room.player_states.get(
                    jersey=current_jersey).player
                self.game_room.save()

            if self.game_room.player_states.get(turn=True).game_state == 30:
                self.game_room.winner = self.game_room.player_states.get(turn=True).player
                self.game_room.status = 'finished'
                self.game_room.save()
                GamesRecords.objects.create(
                    user=self.game_room.winner,
                    game_name=self.game_name,
                    score=self.game_room.player_states.get(turn=True).game_score)

            if self.game_room.winner:
                for pl in self.game_room.player_states.all():
                    if pl.game_score >= self.MIN_SCORE or self.game_room.winner == pl.player:
                        v_score = UserScores.objects.get(user=pl.player).verb_score
                        v_score += pl.game_score
                        UserScores.objects.filter(user=pl.player).update(verb_score=v_score)

                    pl.turn = False
                self.game_room.save()


        elif text_data_json['action'] == 'next_turn':
            select_type = 'next_game_state'
            score = text_data_json['score']
            self.game_room.board_state['q_box'] = False
            current_jersey = self.game_room.player_states.get(turn=True).jersey
            if current_jersey == str(self.game_room.max_players):
                current_jersey = '1'
            else:
                current_jersey = str(int(current_jersey) + 1)
            p_score = self.game_room.player_states.get(turn=True).game_score
            self.game_room.player_states.filter(turn=True).update(
                game_score=p_score + int(score),
                turn=False
            )
            self.game_room.player_states.filter(jersey=current_jersey).update(
                turn=True
            )
            self.game_room.active_turn = self.game_room.player_states.get(
                jersey=current_jersey).player

            self.game_room.board_state['dice_number'] = 0

            self.game_room.save()

        event = {
            'type': select_type,
            'board_state': self.game_room.board_state,
            'active_turn': self.game_room.active_turn.username,
            'game_status': self.game_room.status,
            'winner': self.game_room.winner.username if self.game_room.winner else '',
            'ended_user': ended_user if ended_user else '',
            'quiz': {
                'infinitiv': rand_q.infinitiv if rand_q else '',
                'english': rand_q.english if rand_q else '',
                'turkish': rand_q.turkish if rand_q else '',
            },
            'players': [
                {
                    'id': pl.player.id,
                    'first_name': pl.player.first_name,
                    'username': pl.player.username,
                    'profile_image': pl.player.profile.profile_image.url,
                    'prev_state': pl.prev_state,
                    'game_state': pl.game_state,
                    'game_score': pl.game_score,
                    'color': pl.color,
                    'turn': pl.turn,
                    'dice_history': pl.dice_history
                } for pl in self.game_room.player_states.all()
            ],
        }

        async_to_sync(self.channel_layer.group_send)(
            self.gameroom_id,
            event
        )

    def first_game_state(self, event):
        self.send(text_data=json.dumps(event))

    def roll_dice_state(self, event):
        self.send(text_data=json.dumps(event))

    def next_game_state(self, event):
        self.send(text_data=json.dumps(event))

    def end_game_state(self, event):
        self.send(text_data=json.dumps(event))

    def get_quiz(self):
        all_exm = Verb.objects.all()
        if not all_exm.exists():
            return None
        rand_id = random.randint(1, len(all_exm))
        my_rand = all_exm.get(id=rand_id)
        return my_rand
