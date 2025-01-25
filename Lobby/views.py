from django.shortcuts import render, redirect
from .models import GameRoom, PlayerState
from django.http import JsonResponse
from django.contrib import messages
from collections import defaultdict
import secrets
import string
import asyncio
import random
from django.http import StreamingHttpResponse

g_names = [
    'vokabel',
    'singular_plural',
    'artikel',
    'adjektiv',
    'partizip_II'
]

game_colors = {
    'green': 'success',
    'red': 'danger',
    'blue': 'primary',
    'yellow': 'warning',
}


def generate_random_id(length=6):
    characters = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def create_room(request, game_name):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if game_name in g_names:
        board_state = {
            'dice_number': 0,
            'q_box': False
        }

        while True:
            room_id = generate_random_id()
            is_exist = GameRoom.objects.filter(room_id=room_id, game_name=game_name).exists()
            if not is_exist:
                break

        room = GameRoom.objects.create(
            room_id=room_id,
            game_name=game_name,
            board_state=board_state,
            active_turn=request.user,
            max_players=request.session['max_players'])
        room.players.add(request.user)
        PlayerState.objects.create(
            player=request.user,
            game_room=room,
            color=request.session['chosen_color'],
            turn=True,
            jersey='1'
        )
        return redirect('wait_room', room_id=room.room_id)


def join_room(request, room_id):

    if not request.user.is_authenticated:
        return redirect('user_login')

    try:
        room = GameRoom.objects.get(room_id=room_id)
    except GameRoom.DoesNotExist:
        return redirect('home')

    if request.user not in room.players.all():
        room.players.add(request.user)
    else:
        return redirect('join_room', room_id=room_id)
    if room.players.count() == room.max_players:
        room.status = 'playing'
    room.save()
    this_colors = ['green', 'red', 'blue', 'yellow']
    for col in room.player_states.all():
        this_colors.remove(col.color)

    my_state = PlayerState.objects.create(
        player=request.user,
        game_room=room,
        turn=False,
        jersey=f'{room.players.count()}')

    if request.session['chosen_color'] in this_colors:
        my_state.color = request.session['chosen_color']
    else:
        my_state.color = this_colors[0]
    my_state.save()
    return redirect('wait_room', room_id=room_id)


def wait_room(request, room_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    try:
        room = GameRoom.objects.get(room_id=room_id)
        if request.user in room.players.all():
            return render(request, 'wait_room.html', {'room': room, 'game_colors': game_colors})

    except GameRoom.DoesNotExist:
        return redirect('home')


def check_status(request, room_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    try:
        room = GameRoom.objects.get(room_id=room_id)
        pl_user = [player.username for player in room.players.all()]
        pl_color = [player.color for player in room.player_states.all()]
        players = list(zip(pl_user, pl_color))

        data = {
            'status': room.status,
            'game_name': room.game_name,
            'room_id': room.room_id,
            'players': players
        }
        return JsonResponse(data)
    except GameRoom.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Room not found',
        }, status=404)


def cancel_room(request, room_id):

    if not request.user.is_authenticated:
        return redirect('user_login')

    if (request.method == 'POST') or ('canceled_player' in request.session):
        if 'canceled_player' in request.session:
            del request.session['canceled_player']
        room = GameRoom.objects.get(room_id=room_id)
        if request.user == room.player_states.filter(jersey='1').first().player:
            room.delete()
        else:
            PlayerState.objects.filter(player=request.user).delete()
            room.players.remove(request.user)

        return redirect('home')
    return redirect('wait_room', room_id=room_id)


def index(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
