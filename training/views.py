from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Module, UserModuleProgress
from .forms import QuizScoreForm
from django.db import models

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

@login_required(login_url='login')
def profile(request):
    # Get all module progress for current user
    user_progress = UserModuleProgress.objects.filter(user=request.user)
    
    # Calculate total points (sum of all scores)
    total_points = user_progress.aggregate(total=models.Sum('score'))['total'] or 0
    
    # Count completed modules
    completed_modules = user_progress.aggregate(total=models.Sum('completed'))['total'] or 0
    
    # Total number of modules
    total_modules = Module.objects.count()
    
    # Determine level based on completed modules
    level = "Beginner"
    if completed_modules >= 8:
        level = "Expert"
    elif completed_modules >= 5:
        level = "Advanced"
    elif completed_modules >= 2:
        level = "Intermediate"
    
    context = {
        'user_progress': user_progress,
        'total_points': total_points,
        'completed_modules': completed_modules,
        'total_modules': total_modules,
        'level': level
    }
    return render(request, 'profile.html', context)

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
    """View for the allergy quiz"""
    module = get_object_or_404(Module, slug='allergy_quiz')
    progress, created = UserModuleProgress.objects.get_or_create(
        user=request.user, 
        module=module
    )
    
    if request.method == 'POST':
        form = QuizScoreForm(request.POST)
        if form.is_valid():
            new_score = form.cleaned_data['score']
            
            # Update attempts counter
            progress.attempts += 1
            
            # Only update score if new score is higher
            if new_score > progress.score:
                progress.score = new_score
                if progress.score >= module.passing_score:
                    progress.completed = progress.completed + 1
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            return redirect('allergy_quiz')
    else:
        form = QuizScoreForm(module_slug=module.slug)


    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'allergy_quiz.html', context)





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
