from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Zahlen
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
    all_exm = Zahlen.objects.all()
    if not all_exm.exists():
        return None
    my_rand = random.choice(all_exm)
    return my_rand


def play_game_zahlen_multi(request, game_name='zahlen', room_id=None):

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
        return render(request, 'zahlen_game_multi.html', context=context)
    else:
        messages.warning(request, 'Game is over.', extra_tags='warning')
        return redirect('home')


def play_game_zahlen_one(request, game_name='zahlen'):
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
                                    game_name='Zahlen',
                                    score=player['game_score'])
                                print(request.session['winner'])
                                messages.success(request, f'{player["name"]} won the game', extra_tags='success')
                    if request.session['winner']:
                        for pl in players:
                            if pl['game_score'] >= MIN_SCORE:
                                person = User.objects.get(id=pl['id'])
                                zahl_score = UserScores.objects.get(user=person).zahlen_score
                                zahl_score += pl['game_score']
                                UserScores.objects.filter(user=person).update(zahlen_score=zahl_score)

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
            return render(request, 'zahlen_game_one.html', context=context)
        else:
            request.session['players'] = []
            return redirect(reverse('home'))
    else:
        return redirect(reverse('user_login'))


def add_zahlen(request):
    if request.user.is_superuser:
        my_dict = {
            1900: "eintausendneunhundert",
            1901: "eintausendneunhunderteins",
            1902: "eintausendneunhundertzwei",
            1903: "eintausendneunhundertdrei",
            1904: "eintausendneunhundertvier",
            1905: "eintausendneunhundertfünf",
            1906: "eintausendneunhundertsechs",
            1907: "eintausendneunhundertsieben",
            1908: "eintausendneunhundertacht",
            1909: "eintausendneunhundertneun",
            1910: "eintausendneunhundertzehn",
            1911: "eintausendneunhundertelf",
            1912: "eintausendneunhundertzwölf",
            1913: "eintausendneunhundertdreizehn",
            1914: "eintausendneunhundertvierzehn",
            1915: "eintausendneunhundertfünfzehn",
            1916: "eintausendneunhundertsechzehn",
            1917: "eintausendneunhundertsiebzehn",
            1918: "eintausendneunhundertachtzehn",
            1919: "eintausendneunhundertneunzehn",
            1920: "eintausendneunhundertzwanzig",
            1921: "eintausendneunhunderteinundzwanzig",
            1922: "eintausendneunhundertzweiundzwanzig",
            1923: "eintausendneunhundertdreiundzwanzig",
            1924: "eintausendneunhundertvierundzwanzig",
            1925: "eintausendneunhundertfünfundzwanzig",
            1926: "eintausendneunhundertsechsundzwanzig",
            1927: "eintausendneunhundertsiebenundzwanzig",
            1928: "eintausendneunhundertachtundzwanzig",
            1929: "eintausendneunhundertneunundzwanzig",
            1930: "eintausendneunhundertdreißig",
            1931: "eintausendneunhunderteinunddreißig",
            1932: "eintausendneunhundertzweiunddreißig",
            1933: "eintausendneunhundertdreiunddreißig",
            1934: "eintausendneunhundertvierunddreißig",
            1935: "eintausendneunhundertfünfunddreißig",
            1936: "eintausendneunhundertsechsunddreißig",
            1937: "eintausendneunhundertsiebenunddreißig",
            1938: "eintausendneunhundertachtunddreißig",
            1939: "eintausendneunhundertneununddreißig",
            1940: "eintausendneunhundertvierzig",
            1941: "eintausendneunhunderteinundvierzig",
            1942: "eintausendneunhundertzweiundvierzig",
            1943: "eintausendneunhundertdreiundvierzig",
            1944: "eintausendneunhundertvierundvierzig",
            1945: "eintausendneunhundertfünfundvierzig",
            1946: "eintausendneunhundertsechsundvierzig",
            1947: "eintausendneunhundertsiebenundvierzig",
            1948: "eintausendneunhundertachtundvierzig",
            1949: "eintausendneunhundertneunundvierzig",
            1950: "eintausendneunhundertfünfzig",
            1951: "eintausendneunhunderteinundfünfzig",
            1952: "eintausendneunhundertzweiundfünfzig",
            1953: "eintausendneunhundertdreiundfünfzig",
            1954: "eintausendneunhundertvierundfünfzig",
            1955: "eintausendneunhundertfünfundfünfzig",
            1956: "eintausendneunhundertsechsundfünfzig",
            1957: "eintausendneunhundertsiebenundfünfzig",
            1958: "eintausendneunhundertachtundfünfzig",
            1959: "eintausendneunhundertneunundfünfzig",
            1960: "eintausendneunhundertsechzig",
            1961: "eintausendneunhunderteinundsechzig",
            1962: "eintausendneunhundertzweiundsechzig",
            1963: "eintausendneunhundertdreiundsechzig",
            1964: "eintausendneunhundertvierundsechzig",
            1965: "eintausendneunhundertfünfundsechzig",
            1966: "eintausendneunhundertsechsundsechzig",
            1967: "eintausendneunhundertsiebenundsechzig",
            1968: "eintausendneunhundertachtundsechzig",
            1969: "eintausendneunhundertneunundsechzig",
            1970: "eintausendneunhundertsiebzig",
            1971: "eintausendneunhunderteinundsiebzig",
            1972: "eintausendneunhundertzweiundsiebzig",
            1973: "eintausendneunhundertdreiundsiebzig",
            1974: "eintausendneunhundertvierundsiebzig",
            1975: "eintausendneunhundertfünfundsiebzig",
            1976: "eintausendneunhundertsechsundsiebzig",
            1977: "eintausendneunhundertsiebenundsiebzig",
            1978: "eintausendneunhundertachtundsiebzig",
            1979: "eintausendneunhundertneunundsiebzig",
            1980: "eintausendneunhundertachtzig",
            1981: "eintausendneunhunderteinundachtzig",
            1982: "eintausendneunhundertzweiundachtzig",
            1983: "eintausendneunhundertdreiundachtzig",
            1984: "eintausendneunhundertvierundachtzig",
            1985: "eintausendneunhundertfünfundachtzig",
            1986: "eintausendneunhundertsechsundachtzig",
            1987: "eintausendneunhundertsiebenundachtzig",
            1988: "eintausendneunhundertachtundachtzig",
            1989: "eintausendneunhundertneunundachtzig",
            1990: "eintausendneunhundertneunzig",
            1991: "eintausendneunhunderteinundneunzig",
            1992: "eintausendneunhundertzweiundneunzig",
            1993: "eintausendneunhundertdreiundneunzig",
            1994: "eintausendneunhundertvierundneunzig",
            1995: "eintausendneunhundertfünfundneunzig"
        }
        for k, v in my_dict.items():
            is_exist = Zahlen.objects.filter(number=k).exists()
            if not is_exist:
                Zahlen.objects.create(
                    number=k,
                    german=v,
                )
            else:
                messages.warning(request, 'Number already exists', extra_tags='warning')
                return redirect(reverse('home'))
        messages.success(request, 'Number added successfully', extra_tags='success')
        return redirect(reverse('home'))
    else:
        messages.warning(request, 'You are not admin!', extra_tags='warning')
        return redirect(reverse('home'))
