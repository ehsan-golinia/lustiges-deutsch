from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

# Create your views here


def custom_page_not_found(request, exception):
    """Custom 404 view that redirects to the homepage."""
    return redirect('/')


g_names = [
    'vokabel',
    'singular_plural',
    'artikel',
    'adjektiv',
    'partizip_II'
]


def home(request):
    return render(request, 'home.html')


def playervsplayer(request, game_name='vokabel'):
    if request.user.is_authenticated:
        if game_name in g_names:
            p_id = request.user.id
            p_name = request.user.first_name
            p_photo = request.user.profile.profile_image.url

            if request.method == 'POST':
                request.session['playerCount'] = int(request.POST['radioOption'])
                colors = ['green', 'red', 'blue', 'yellow', 'orange', 'pink', 'purple']
                players = [{'id': p_id, 'name': p_name, 'color': 'green', 'prev_state': 0, 'game_state': 0, 'game_score': 0, 'dice_history':[], 'turn': True, 'jersey': '0', 'photo': p_photo}]
                if int(request.POST['radioOption']) == 2:
                    players.append({'id': 12, 'name': 'Mahsa', 'color': 'red', 'prev_state': 0, 'game_state': 0, 'game_score': 0, 'dice_history':[], 'turn': False, 'jersey': '1', 'photo': '/media/profile_images/mahsa_waPAPyI.png'})
                request.session['players'] = players
                request.session['dice_number'] = 0
                request.session['winner'] = ''
                request.session['q_box'] = False
                return redirect(f'/{game_name}/playgame/')
            return render(request, 'playervsplayer.html')
        else:
            return redirect(reverse('home'))
    else:
        return redirect(reverse('user_login'))


def all_ranking(request):
    return render(request, 'all_ranking.html')
