from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from Vokabel.models import Vokabel
from Singular_Plural.models import SingularPlural
from accounts.models import GamesRecords
from Lobby.models import GameRoom, PlayerState
from django.contrib.auth.models import User
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import random


channel_layer = get_channel_layer()


def send_game_update(room):
    async_to_sync(channel_layer.group_send)(
        f"game_{room.room_id}",
        {
            'type': 'game_message',
            'action': 'update_game_state',
            'payload': {
                'board_state': room.board_state,
                'players': [
                    {
                        'username': player.player.username,
                        'game_state': player.game_state,
                        'score': player.game_score,
                        'color': player.color
                    } for player in room.player_states.all()
                ]
            }
        }
    )

# Create your views here.

cell_size = 52
board_data = [
    {'value': 0, 'x': 2, 'y': 6, 'special': 'START'},
    {'value': 1, 'x': 2, 'y': 5, 'special': '1'},
    {'value': 2, 'x': 2, 'y': 4, 'special': '2'},
    {'value': 3, 'x': 2, 'y': 3, 'special': '3'},
    {'value': 4, 'x': 2, 'y': 2, 'special': '4'},
    {'value': 5, 'x': 2, 'y': 1, 'special': '5'},
    {'value': 6, 'x': 2, 'y': 0, 'special': '6'},
    {'value': 7, 'x': 3, 'y': 0, 'special': '7'},
    {'value': 8, 'x': 4, 'y': 0, 'special': '8'},
    {'value': 9, 'x': 4, 'y': 1, 'special': '9'},
    {'value': 10, 'x': 4, 'y': 2, 'special': '10'},
    {'value': 11, 'x': 4, 'y': 3, 'special': '11'},
    {'value': 12, 'x': 4, 'y': 4, 'special': '12'},
    {'value': 13, 'x': 4, 'y': 5, 'special': '13'},
    {'value': 14, 'x': 4, 'y': 6, 'special': '14'},
    {'value': 15, 'x': 5, 'y': 6, 'special': '15'},
    {'value': 16, 'x': 6, 'y': 6, 'special': '16'},
    {'value': 17, 'x': 6, 'y': 5, 'special': '17'},
    {'value': 18, 'x': 6, 'y': 4, 'special': '18'},
    {'value': 19, 'x': 6, 'y': 3, 'special': '19'},
    {'value': 20, 'x': 6, 'y': 2, 'special': '20'},
    {'value': 21, 'x': 6, 'y': 1, 'special': '21'},
    {'value': 22, 'x': 6, 'y': 0, 'special': '22'},
    {'value': 23, 'x': 7, 'y': 0, 'special': '23'},
    {'value': 24, 'x': 8, 'y': 0, 'special': '24'},
    {'value': 25, 'x': 8, 'y': 1, 'special': '25'},
    {'value': 26, 'x': 8, 'y': 2, 'special': '26'},
    {'value': 27, 'x': 8, 'y': 3, 'special': '27'},
    {'value': 28, 'x': 8, 'y': 4, 'special': '28'},
    {'value': 29, 'x': 8, 'y': 5, 'special': '29'},
    {'value': 30, 'x': 8, 'y': 6, 'special': 'END'},
]

MIN_SCORE = 10

game_colors = {
    'green': 'success',
    'red': 'danger',
    'blue': 'primary',
    'yellow': 'warning',
}


def get_quiz():
    all_exm = Vokabel.objects.all()
    if not all_exm.exists():
        return None, None
    rand_id = random.randint(1, len(all_exm))
    my_rand = all_exm.get(id=rand_id)
    return my_rand


def play_game_vokabel_multi(request, game_name='vokabel', room_id=None):

    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))

    try:
        room = GameRoom.objects.get(room_id=room_id, game_name=game_name)
    except GameRoom.DoesNotExist:
        return redirect('home')

    if request.user not in room.players.all():
        return redirect('home')

    if not room.winner and room.status == 'playing':
    #     player_count = room.max_players
    #     players = room.player_states.all()
    #     dice_number = room.board_state['dice_number']
    #     q_box = room.board_state['q_box']
    #     rand_example = None
    #
        if request.method == 'POST':
            end_game = request.POST.get('end_game')
            if end_game:
                request.session['canceled_player'] = end_game
                return redirect('cancel_room', room_id=room.room_id)
    #
    #         next_turn = request.POST.get('next_turn')
    #         print(f'Bizim = {next_turn}')
    #         if next_turn is not None:
    #             room.board_state['q_box'] = False
    #             for player in players:
    #                 player.prev_state = player.game_state
    #
    #                 if player.turn:
    #                     player.game_score += int(next_turn)
    #                     if len(players) > 1:
    #                         player.turn = False
    #                 else:
    #                     player.turn = True
    #
    #         else:
    #             dice_number = random.randint(1, 3)
    #             room.board_state['dice_number'] = dice_number
    #             send_game_update(room)
    #
    #             for player in players:
    #                 player.prev_state = player.game_state
    #                 if player.turn:
    #                     if (player.game_state + dice_number) <= 30:
    #                         player.game_state += dice_number
    #                         player.dice_history.append(dice_number)
    #                         if player.game_state != 30:
    #                             q_box = True
    #                             rand_example = get_quiz()
    #
    #                     if player.game_state == 30:
    #                         room.winner = player.player
    #                         winner = User.objects.get(id=player.player.id)
    #                         GamesRecords.objects.create(
    #                             user=winner,
    #                             game_name='Vokabel',
    #                             score=player.game_score)
    #                         print(room.winner)
    #                         messages.success(request, f'{room.winner.first_name} won the game', extra_tags='success')
    #             if room.winner:
    #                 for pl in players:
    #                     if pl.game_score >= MIN_SCORE:
    #                         person = User.objects.get(id=pl.player.id)
    #                         person.profile.total_scores += pl.game_score
    #                         person.profile.save()
    #                         person.scores.vokabel_score += pl.game_score
    #                         person.scores.save()
    #
    #     circle_data = []
    #
    #     for pl in players:
    #         circle_data.append(
    #             {
    #                 'value': f'p{pl.player.id}',
    #                 'fill': f'{pl.color}',
    #                 'px': (board_data[pl.prev_state]['x'] * cell_size) + (cell_size / 2),
    #                 'x': (board_data[pl.game_state]['x'] * cell_size) + (cell_size / 2),
    #                 'py': (board_data[pl.prev_state]['y'] * cell_size) + (cell_size / 2),
    #                 'y': (board_data[pl.game_state]['y'] * cell_size) + (cell_size / 2)
    #             }
    #         )
    #
    #     contextt = {
    #         'room': room,
    #         'players': players,
    #         'game_name': game_name,
    #         'player_count': player_count,
    #         'cell_size': cell_size,
    #         'board_data': board_data,
    #         'circle_data': circle_data,
    #         'dice_number': dice_number,
    #         'q_box': q_box,
    #         'rand_example': rand_example,
    #         'game_colors': game_colors
    #     }
    context = {
        'cell_size': cell_size,
        'board_data': board_data,
        'room_id': room.room_id,
        'game_name': room.game_name,
        'game_colors': game_colors
    }
    return render(request, 'vokabel_game.html', context=context)
    # else:
    #     room.status = 'finished'
    #     return redirect(reverse('home'))


def play_game_vokabel(request, game_name='vokabel'):
    if request.user.is_authenticated:
        if not request.session['players']:
            return redirect(reverse('home'))
        if not request.session['winner']:
            player_count = request.session.get('playerCount', 1)
            players = request.session.get('players', [])
            dice_number = request.session.get('dice_number', 0)
            q_box = request.session.get('q_box', False)
            rand_example = None

            if request.method == 'POST':

                # Retrieve the player ID from the form data
                player_jersey = request.POST.get('player_jersey')
                end_game = request.POST.get('end_game')
                if end_game:
                    request.session['players'] = []
                    return redirect(reverse('home'))

                next_turn = request.POST.get('next_turn')
                print(f'Bizim = {next_turn}')
                if next_turn is not None:
                    request.session['q_box'] = False
                    for player in players:
                        player['prev_state'] = player['game_state']

                        if player['turn']:
                            player['game_score'] += int(next_turn)
                            if len(players) > 1:
                                player['turn'] = False
                        else:
                            player['turn'] = True

                else:
                    dice_number = random.randint(1, 3)
                    request.session['dice_number'] = dice_number

                    for player in players:
                        player['prev_state'] = player['game_state']
                        if player['turn']:
                            if (player['game_state'] + dice_number) <= 30:
                                player['game_state'] += dice_number
                                player['dice_history'].append(dice_number)
                                if player['game_state'] != 30:
                                    q_box = True
                                    rand_example = get_quiz()

                            if player['game_state'] == 30:
                                request.session['winner'] = player['name']
                                winner = User.objects.get(id=player['id'])
                                GamesRecords.objects.create(
                                    user=winner,
                                    game_name='Vokabel',
                                    score=player['game_score'])
                                print(request.session['winner'])
                                messages.success(request, f'{player["name"]} won the game', extra_tags='success')
                    if request.session['winner']:
                        for pl in players:
                            if pl['game_score'] >= MIN_SCORE:
                                person = User.objects.get(id=pl['id'])
                                person.profile.total_scores += pl['game_score']
                                person.profile.save()
                                person.scores.vokabel_score += pl['game_score']
                                person.scores.save()

            request.session['players'] = players
            circle_data = []

            for pl in players:
                circle_data.append(
                    {
                        'value': f'p{pl['id']}',
                        'fill': f'{pl['color']}',
                        'px': (board_data[pl['prev_state']]['x'] * cell_size) + (cell_size / 2),
                        'x': (board_data[pl['game_state']]['x'] * cell_size) + (cell_size / 2),
                        'py': (board_data[pl['prev_state']]['y'] * cell_size) + (cell_size / 2),
                        'y': (board_data[pl['game_state']]['y'] * cell_size) + (cell_size / 2)
                    }
                )

            context = {
                'players': players,
                'game_name': game_name,
                'player_count': player_count,
                'cell_size': cell_size,
                'board_data': board_data,
                'circle_data': circle_data,
                'dice_number': dice_number,
                'q_box': q_box,
                'rand_example': rand_example,
                'game_colors': game_colors
            }
            return render(request, 'vokabel_game_one.html', context=context)
        else:
            request.session['players'] = []
            return redirect(reverse('home'))
    else:
        return redirect(reverse('user_login'))


def add_vokabel(request):
    if request.user.is_superuser:
        my_german = "Der Eingang"
        is_exist = Vokabel.objects.filter(german=my_german).exists()
        if not is_exist:
            vokabel = Vokabel.objects.create(
                german=my_german,
                english="the entrance",
                turkish="giriş"
            )
            SingularPlural.objects.create(
                singular="Der Eingang",
                plural="Die Eingänge",
                vokabel=vokabel
            )
            messages.success(request, 'Vokabel added successfully', extra_tags='success')
        else:
            messages.error(request, 'Vokabel already exists', extra_tags='error')
        return redirect(reverse('home'))
    else:
        return redirect(reverse('user_login'))
