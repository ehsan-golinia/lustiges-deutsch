from django.shortcuts import render, redirect
from .models import GameRoom, PlayerState
from django.http import JsonResponse
from django.contrib import messages
from collections import defaultdict
import secrets
import string
import asyncio
import random
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from LustigesDeutsch.constants import game_colors, g_names


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
        players = []
        for pl in room.player_states.all():
            players.append({
                'username': pl.player.username,
                'color': pl.color
            })

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

    if request.method == 'POST':
        room = GameRoom.objects.get(room_id=room_id)
        if request.user == room.player_states.filter(jersey='1').first().player:
            room.delete()
        else:
            PlayerState.objects.filter(player=request.user).delete()
            room.players.remove(request.user)

        return redirect('home')
    else:
        if GameRoom.objects.filter(room_id=room_id, status='cancelled').exists():
            if request.user in GameRoom.objects.get(room_id=room_id, status='cancelled').players.all():
                GameRoom.objects.filter(room_id=room_id, status='cancelled').delete()
        return redirect('home')


def finish_room(request, game_name, room_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    if GameRoom.objects.filter(room_id=room_id, game_name=game_name, status='finished').exists():
        if request.user in GameRoom.objects.get(room_id=room_id, game_name=game_name, status='finished').players.all():
            if request.method == 'POST':
                end_game = request.POST.get('end_game')
                if end_game is not None:
                    GameRoom.objects.filter(room_id=room_id, game_name=game_name, status='finished').delete()
                messages.success(request, 'Game finished', extra_tags='success')
                return redirect('home')
            this_room = GameRoom.objects.get(room_id=room_id, game_name=game_name, status='finished')
            players = this_room.player_states.all()
            return render(request, 'finish.html', {'room': this_room, 'players': players, 'game_colors': game_colors})

    messages.success(request, 'Game finished', extra_tags='success')
    return redirect('home')


def index(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
