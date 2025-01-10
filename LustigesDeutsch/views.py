from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here


def home(request):
    return render(request, 'home.html')


def playervsplayer(request, gameName = 'vokabel'):
    request.session.flush()
    if request.method == 'POST':
        request.session['radioOption'] = request.POST['radioOption']
        return redirect(reverse(f'{gameName}:playervsplayer'))
        # print(request.session['radioOption'])
    return render(request, 'playervsplayer.html')

