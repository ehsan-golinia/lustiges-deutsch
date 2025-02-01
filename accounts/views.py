from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UpdateForm
from django.contrib.auth.models import User
from .models import UserProfile, UserScores
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully', extra_tags='success')
                    return redirect(reverse('home'))
                else:
                    messages.error(request, 'Invalid username or password', extra_tags='danger')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password2']:
                messages.error(request, 'Passwords do not match!', extra_tags='danger')
            else:
                if User.objects.filter(username=cd['username']).exists():
                    messages.error(request, 'Username already exists!', extra_tags='danger')
                else:
                    user = User.objects.create_user(username=cd['username'], password=cd['password'])
                    user.first_name = cd.get('first_name', '')
                    user.last_name = cd.get('last_name', '')
                    user.save()
                    # Create the UserProfile
                    UserProfile.objects.create(user=user)
                    UserScores.objects.create(user=user)
                    messages.success(request, 'Account created successfully', extra_tags='success')
                    return redirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully', extra_tags='success')
    # go to current page
    return redirect(reverse('home'))


def user_settings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
                    messages.error(request, 'Passwords do not match!', extra_tags='danger')
                elif cd['password'] and (not cd['password2']):
                    messages.error(request, 'Repeat your password!', extra_tags='danger')
                elif (not cd['password']) and cd['password2']:
                    messages.error(request, 'Repeat your password!', extra_tags='danger')
                elif (cd['username'] != request.user.username) and User.objects.filter(username=cd['username']).exists():
                    messages.error(request, 'Username already exists!', extra_tags='danger')
                else:
                    user = request.user
                    user.first_name = cd['first_name']
                    user.last_name = cd['last_name']
                    user.email = cd['email']
                    if cd['username'] != user.username:
                        user.username = cd['username']
                    if cd['password']:
                        user.set_password(cd['password'])
                    user.save()
                    messages.success(request, 'Profile updated successfully', extra_tags='success')
                    return redirect(reverse('home'))

        else:
            form = UpdateForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'username': request.user.username,
            })

        return render(request, 'settings.html', {'form': form})
    else:
        return redirect(reverse('user_login'))


def user_profile(request):
    this_user = UserScores.objects.get(user=request.user)
    context = {
        'this_user': ''
    }
    return render(request, 'profile.html', {'form': context})
