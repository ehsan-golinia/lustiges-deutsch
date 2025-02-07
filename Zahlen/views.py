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
    rand_id = random.randint(1, len(all_exm))
    my_rand = all_exm.get(id=rand_id)
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
            700: "siebenhundert",
            701: "siebenhunderteins",
            702: "siebenhundertzwei",
            703: "siebenhundertdrei",
            704: "siebenhundertvier",
            705: "siebenhundertfünf",
            706: "siebenhundertsechs",
            707: "siebenhundertsieben",
            708: "siebenhundertacht",
            709: "siebenhundertneun",
            710: "siebenhundertzehn",
            711: "siebenhundertelf",
            712: "siebenhundertzwölf",
            713: "siebenhundertdreizehn",
            714: "siebenhundertvierzehn",
            715: "siebenhundertfünfzehn",
            716: "siebenhundertsechzehn",
            717: "siebenhundertsiebzehn",
            718: "siebenhundertachtzehn",
            719: "siebenhundertneunzehn",
            720: "siebenhundertzwanzig",
            721: "siebenhunderteinundzwanzig",
            722: "siebenhundertzweiundzwanzig",
            723: "siebenhundertdreiundzwanzig",
            724: "siebenhundertvierundzwanzig",
            725: "siebenhundertfünfundzwanzig",
            726: "siebenhundertsechsundzwanzig",
            727: "siebenhundertsiebenundzwanzig",
            728: "siebenhundertachtundzwanzig",
            729: "siebenhundertneunundzwanzig",
            730: "siebenhundertdreißig",
            731: "siebenhunderteinunddreißig",
            732: "siebenhundertzweiunddreißig",
            733: "siebenhundertdreiunddreißig",
            734: "siebenhundertvierunddreißig",
            735: "siebenhundertfünfunddreißig",
            736: "siebenhundertsechsunddreißig",
            737: "siebenhundertsiebenunddreißig",
            738: "siebenhundertachtunddreißig",
            739: "siebenhundertneununddreißig",
            740: "siebenhundertvierzig",
            741: "siebenhunderteinundvierzig",
            742: "siebenhundertzweiundvierzig",
            743: "siebenhundertdreiundvierzig",
            744: "siebenhundertvierundvierzig",
            745: "siebenhundertfünfundvierzig",
            746: "siebenhundertsechsundvierzig",
            747: "siebenhundertsiebenundvierzig",
            748: "siebenhundertachtundvierzig",
            749: "siebenhundertneunundvierzig",
            750: "siebenhundertfünfzig",
            751: "siebenhunderteinundfünfzig",
            752: "siebenhundertzweiundfünfzig",
            753: "siebenhundertdreiundfünfzig",
            754: "siebenhundertvierundfünfzig",
            755: "siebenhundertfünfundfünfzig",
            756: "siebenhundertsechsundfünfzig",
            757: "siebenhundertsiebenundfünfzig",
            758: "siebenhundertachtundfünfzig",
            759: "siebenhundertneunundfünfzig",
            760: "siebenhundertsechzig",
            761: "siebenhunderteinundsechzig",
            762: "siebenhundertzweiundsechzig",
            763: "siebenhundertdreiundsechzig",
            764: "siebenhundertvierundsechzig",
            765: "siebenhundertfünfundsechzig",
            766: "siebenhundertsechsundsechzig",
            767: "siebenhundertsiebenundsechzig",
            768: "siebenhundertachtundsechzig",
            769: "siebenhundertneunundsechzig",
            770: "siebenhundertsiebzig",
            771: "siebenhunderteinundsiebzig",
            772: "siebenhundertzweiundsiebzig",
            773: "siebenhundertdreiundsiebzig",
            774: "siebenhundertvierundsiebzig",
            775: "siebenhundertfünfundsiebzig",
            776: "siebenhundertsechsundsiebzig",
            777: "siebenhundertsiebenundsiebzig",
            778: "siebenhundertachtundsiebzig",
            779: "siebenhundertneunundsiebzig",
            780: "siebenhundertachtzig",
            781: "siebenhunderteinundachtzig",
            782: "siebenhundertzweiundachtzig",
            783: "siebenhundertdreiundachtzig",
            784: "siebenhundertvierundachtzig",
            785: "siebenhundertfünfundachtzig",
            786: "siebenhundertsechsundachtzig",
            787: "siebenhundertsiebenundachtzig",
            788: "siebenhundertachtundachtzig",
            789: "siebenhundertneunundachtzig",
            790: "siebenhundertneunzig",
            791: "siebenhunderteinundneunzig",
            792: "siebenhundertzweiundneunzig",
            793: "siebenhundertdreiundneunzig",
            794: "siebenhundertvierundneunzig",
            795: "siebenhundertfünfundneunzig",
            796: "siebenhundertsechsundneunzig",
            797: "siebenhundertsiebenundneunzig",
            798: "siebenhundertachtundneunzig",
            799: "siebenhundertneunundneunzig",
            800: "achthundert",
            801: "achthunderteins",
            802: "achthundertzwei",
            803: "achthundertdrei",
            804: "achthundertvier",
            805: "achthundertfünf",
            806: "achthundertsechs",
            807: "achthundertsieben",
            808: "achthundertacht",
            809: "achthundertneun",
            810: "achthundertzehn",
            811: "achthundertelf",
            812: "achthundertzwölf",
            813: "achthundertdreizehn",
            814: "achthundertvierzehn",
            815: "achthundertfünfzehn",
            816: "achthundertsechzehn",
            817: "achthundertsiebzehn",
            818: "achthundertachtzehn",
            819: "achthundertneunzehn",
            820: "achthundertzwanzig",
            821: "achthunderteinundzwanzig",
            822: "achthundertzweiundzwanzig",
            823: "achthundertdreiundzwanzig",
            824: "achthundertvierundzwanzig",
            825: "achthundertfünfundzwanzig",
            826: "achthundertsechsundzwanzig",
            827: "achthundertsiebenundzwanzig",
            828: "achthundertachtundzwanzig",
            829: "achthundertneunundzwanzig",
            830: "achthundertdreißig",
            831: "achthunderteinunddreißig",
            832: "achthundertzweiunddreißig",
            833: "achthundertdreiunddreißig",
            834: "achthundertvierunddreißig",
            835: "achthundertfünfunddreißig",
            836: "achthundertsechsunddreißig",
            837: "achthundertsiebenunddreißig",
            838: "achthundertachtunddreißig",
            839: "achthundertneununddreißig",
            840: "achthundertvierzig",
            841: "achthunderteinundvierzig",
            842: "achthundertzweiundvierzig",
            843: "achthundertdreiundvierzig",
            844: "achthundertvierundvierzig",
            845: "achthundertfünfundvierzig",
            846: "achthundertsechsundvierzig",
            847: "achthundertsiebenundvierzig",
            848: "achthundertachtundvierzig",
            849: "achthundertneunundvierzig",
            850: "achthundertfünfzig",
            851: "achthunderteinundfünfzig",
            852: "achthundertzweiundfünfzig",
            853: "achthundertdreiundfünfzig",
            854: "achthundertvierundfünfzig",
            855: "achthundertfünfundfünfzig",
            856: "achthundertsechsundfünfzig",
            857: "achthundertsiebenundfünfzig",
            858: "achthundertachtundfünfzig",
            859: "achthundertneunundfünfzig",
            860: "achthundertsechzig",
            861: "achthunderteinundsechzig",
            862: "achthundertzweiundsechzig",
            863: "achthundertdreiundsechzig",
            864: "achthundertvierundsechzig",
            865: "achthundertfünfundsechzig",
            866: "achthundertsechsundsechzig",
            867: "achthundertsiebenundsechzig",
            868: "achthundertachtundsechzig",
            869: "achthundertneunundsechzig",
            870: "achthundertsiebzig",
            871: "achthunderteinundsiebzig",
            872: "achthundertzweiundsiebzig",
            873: "achthundertdreiundsiebzig",
            874: "achthundertvierundsiebzig",
            875: "achthundertfünfundsiebzig",
            876: "achthundertsechsundsiebzig",
            877: "achthundertsiebenundsiebzig",
            878: "achthundertachtundsiebzig",
            879: "achthundertneunundsiebzig",
            880: "achthundertachtzig",
            881: "achthunderteinundachtzig",
            882: "achthundertzweiundachtzig",
            883: "achthundertdreiundachtzig",
            884: "achthundertvierundachtzig",
            885: "achthundertfünfundachtzig",
            886: "achthundertsechsundachtzig",
            887: "achthundertsiebenundachtzig",
            888: "achthundertachtundachtzig",
            889: "achthundertneunundachtzig",
            890: "achthundertneunzig",
            891: "achthunderteinundneunzig",
            892: "achthundertzweiundneunzig",
            893: "achthundertdreiundneunzig",
            894: "achthundertvierundneunzig",
            895: "achthundertfünfundneunzig",
            896: "achthundertsechsundneunzig",
            897: "achthundertsiebenundneunzig",
            898: "achthundertachtundneunzig",
            899: "achthundertneunundneunzig"
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
