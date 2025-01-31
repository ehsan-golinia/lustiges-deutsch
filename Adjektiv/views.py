from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Adjektiv
from accounts.models import GamesRecords, UserScores
from Lobby.models import GameRoom, PlayerState
from django.contrib.auth.models import User
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from LustigesDeutsch.constants import MIN_SCORE, MAX_DICE, game_colors, cell_size, board_data
import random


# Create your views here.


def get_quiz():
    all_exm = Adjektiv.objects.all()
    if not all_exm.exists():
        return None
    rand_id = random.randint(1, len(all_exm))
    my_rand = all_exm.get(id=rand_id)
    return my_rand


def play_game_adjektiv_multi(request, game_name='adjektiv', room_id=None):

    if not request.user.is_authenticated:
        messages.warning(request, 'You are not logged in.', extra_tags='warning')
        return redirect(reverse('user_login'))

    try:
        room = GameRoom.objects.get(room_id=room_id, game_name=game_name)
    except GameRoom.DoesNotExist:
        messages.warning(request, 'Room not found.', extra_tags='warning')
        return redirect('home')

    if request.user not in room.players.all():
        messages.error(request, 'You are not a member of this room.', extra_tags='error')
        return redirect('home')

    if not room.winner and room.status == 'playing':

        context = {
            'cell_size': cell_size,
            'board_data': board_data,
            'room_id': room.room_id,
            'game_name': room.game_name,
            'game_colors': game_colors,
            'MAX_DICE': MAX_DICE
        }
        return render(request, 'adjektiv_game_multi.html', context=context)
    else:
        messages.warning(request, 'Game is over.', extra_tags='warning')
        return redirect('home')


def play_game_adjektiv_one(request, game_name='adjektiv'):
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
                    dice_number = random.randint(1, MAX_DICE)
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
                                    game_name='Adjektiv',
                                    score=player['game_score'])
                                print(request.session['winner'])
                                messages.success(request, f'{player["name"]} won the game', extra_tags='success')
                    if request.session['winner']:
                        for pl in players:
                            if pl['game_score'] >= MIN_SCORE:
                                person = User.objects.get(id=pl['id'])
                                adj_score = UserScores.objects.get(user=person).adjektiv_score
                                adj_score += pl['game_score']
                                UserScores.objects.filter(user=person).update(adjektiv_score=adj_score)

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
            return render(request, 'adjektiv_game_one.html', context=context)
        else:
            request.session['players'] = []
            return redirect(reverse('home'))
    else:
        return redirect(reverse('user_login'))


def add_adjektiv(request):
    if request.user.is_superuser:
        my_positiv = "beruflich"
        is_exist = Adjektiv.objects.filter(positiv=my_positiv).exists()
        if not is_exist:
            Adjektiv.objects.create(
                english="occupational",
                turkish="mesleki",
                positiv=my_positiv,
                komparativ="-",
                superlativ="-"
            )
            messages.success(request, 'Adjektiv added successfully', extra_tags='success')
        else:
            messages.warning(request, 'Adjektiv already exists', extra_tags='warning')
        return redirect(reverse('home'))
    else:
        messages.warning(request, 'You are not admin!', extra_tags='warning')
        return redirect(reverse('home'))
