from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def modules(request):
    return render(request, 'modules.html')

@login_required
def scenarios(request):
    return render(request, 'scenarios.html')

@login_required
def achievements(request):
    return render(request, 'achievements.html')

@login_required
def leaderboard(request):
    return render(request, 'leaderboard.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def burns_learning(request):
    return render(request, 'burns_learning.html')

def burns_quiz(request):
    return render(request, 'burns_quiz.html')

def wounds_learning(request):
    return render(request, 'wounds_learning.html')

def wounds_quiz(request):
    return render(request, 'wounds_quiz.html')

def fractures_learning(request):
    return render(request, 'fractures_and_sprains_learning.html')

def fractures_quiz(request):
    return render(request, 'fractures_and_sprains_quiz.html')

def cardiac_emergencies_learning(request):
    return render(request, 'cardiac_emergencies_learning.html')

def cardiac_emergencies_quiz(request):
    return render(request, 'cardiac_emergencies_quiz.html')

def choking_learning(request):
    return render(request, 'choking_learning.html')

def choking_quiz(request):
    return render(request, 'choking_quiz.html')

def heat_learning(request):
    return render(request, 'heat_learning.html')

def heat_quiz(request):
    return render(request, 'heat_quiz.html')

def cold_learning(request):
    return render(request, 'cold_learning.html')

def cold_quiz(request):
    return render(request, 'cold_quiz.html')

def poison_learning(request):
    return render(request, 'poison_learning.html')

def poison_quiz(request):
    return render(request, 'poison_quiz.html')

def venom_learning(request):
    return render(request, 'venom_learning.html')

def venom_quiz(request):
    return render(request, 'venom_quiz.html')

def allergy_learning(request):
    return render(request, 'allergy_learning.html')

def allergy_quiz(request):
    return render(request, 'allergy_quiz.html')









def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        return redirect('profile')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')
