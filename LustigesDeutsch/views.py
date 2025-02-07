from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from accounts.models import GamesRecords, UserScores
from Lobby.models import GameRoom
from .constants import g_names

# Create your views here


def custom_page_not_found(request, exception):
    """Custom 404 view that redirects to the homepage."""
    return redirect('/')


def home(request):
    return render(request, 'home.html')


def playervsplayer(request, game_name='vokabel'):
    if not request.user.is_authenticated:
        return redirect('user_login')
    if game_name in g_names:
        if request.method == 'POST':
            chosen_color = request.POST['color']
            request.session['chosen_color'] = chosen_color
            create_new = request.POST.get('create_new')
            join_game = request.POST.get('join_game')
            if create_new is not None:
                player_count = int(request.POST['maxplayers'])
                request.session['max_players'] = player_count
                if player_count > 1:
                    return redirect('create_room', game_name=game_name)
                else:
                    p_id = request.user.id
                    p_name = request.user.first_name
                    p_photo = request.user.profile.profile_image.url
                    players = [{'id': p_id, 'name': p_name, 'color': chosen_color, 'prev_state': 0, 'game_state': 0,
                                'game_score': 0, 'dice_history': [], 'turn': True, 'jersey': '0', 'photo': p_photo}]
                    request.session['players'] = players
                    request.session['dice_number'] = 0
                    request.session['winner'] = ''
                    request.session['q_box'] = False
                    return redirect(f'/{game_name}/playgame/')

            if join_game is not None:
                get_room_id = request.POST['room_id']
                if get_room_id:
                    try:
                        room = GameRoom.objects.get(room_id=get_room_id, game_name=game_name, status='waiting')
                        print(room.room_id)
                        return redirect('join_room', room_id=room.room_id)
                    except GameRoom.DoesNotExist:
                        messages.warning(request, 'There is no game with this ID', extra_tags='warning')
                else:
                    try:
                        room = GameRoom.objects.get(game_name=game_name, status='waiting')
                        return redirect('join_room', room_id=room.room_id)
                    except GameRoom.DoesNotExist:
                        messages.warning(request, 'There is no active game', extra_tags='warning')

        return render(request, 'playervsplayer.html')
    else:
        return redirect('home')


def all_ranking(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    this_users = UserScores.objects.all()
    # games = GamesRecords.filter(user= )
    all_players = []
    for u in this_users:
        user_games = GamesRecords.objects.filter(user=u.user).count()
        all_players.append({
            'total_score': u.total_scores(),
            'username': u.user.username,
            'name': u.user.first_name,
            'winner': user_games
        })
    context = {'all_players': sorted(all_players, key=lambda x: x['total_score'], reverse=True)}
    return render(request, 'all_ranking.html', context)
