from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Module, UserModuleProgress,Achievement,UserAchievement,Scenario,UserScenarioProgress
from .forms import QuizScoreForm, ScenarioScoreForm
from django.db import models
from django.db.models import Sum, Count
import logging
import time

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

@login_required
def achievements(request):
    # Load all achievements and user's current achievements
    print(">> Achievements view loaded")
    user_progress = UserModuleProgress.objects.filter(user=request.user)
    total_points = user_progress.aggregate(total=models.Sum('score'))['total'] or 0
    completed_modules = user_progress.filter(completed=True)
    completed_modules_count = user_progress.filter(completed=True).count()
    completed_scenarios_count = UserScenarioProgress.objects.filter(user=request.user, completed=True).count()

    all_achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user)
    earned_ids = {ua.achievement.id for ua in user_achievements}

    # Prepare achievement lookup
    achievements_by_title = {a.title: a for a in all_achievements}

    def unlock(title, condition):
        print(f"Checking unlock: {title}, Condition: {condition}")
        if title in achievements_by_title:
            achievement = achievements_by_title[title]
            print(f"Achievement found: {achievement}")
            if condition and achievement.id not in earned_ids:
                print("Unlocking achievement...")
                UserAchievement.objects.create(user=request.user, achievement=achievement)
                messages.success(request, f"Achievement Unlocked: {title}!")
                earned_ids.add(achievement.id)
            else:
                print("Already earned or condition false.")
        else:
            print(f"Title '{title}' not found in achievements_by_title")


    # Achievement logic
    unlock('First Steps', completed_modules_count >= 1)
    unlock('Life Saver', completed_modules_count == 10)
    unlock('Quick Thinker', user_progress.filter(completed=True, time_spent__lt=30).exists())
    unlock('Expert Medic', total_points == 1000)
    unlock('All Star', completed_modules_count == 10 and completed_scenarios_count == 3)
    unlock('Academic Ace', completed_modules_count >= 5)
    unlock('Simulation Pro',completed_scenarios_count >= 3)
    unlock('Trailblazer',completed_scenarios_count >= 1)
    for progress in completed_modules:
        unlock('Perfect Score',progress.score == 100)

    

    # Prepare context for template
    achievements_data = [
        {
            'achievement': ach,
            'achieved': ach.id in earned_ids
        }
        for ach in all_achievements
    ]

    context = {
        'achievements': achievements_data,
        'unlocked_count': len(earned_ids),
        'earned_ids': earned_ids,
    }
    print("Context being sent to template:", context)

    return render(request, 'achievements.html', context)

@login_required
def modules(request):
    user = request.user
    completed_progress = UserModuleProgress.objects.filter(user=user, completed=True)
    completed_modules = set(progress.module.title for progress in completed_progress)

    context = {
        'completed_modules': completed_modules,
    }

    return render(request, 'modules.html', context)

@login_required
def scenarios(request):
    return render(request, 'scenarios.html')

@login_required(login_url='login')
def leaderboard(request):
    # Get all users and annotate their total score and completed modules
    users_with_scores = (
        User.objects.annotate(
            total_points=Sum('module_progress__score'),
            completed_modules=Count('module_progress', filter=models.Q(module_progress__completed=True))
        )
        .order_by('-total_points')
    )

    total_items = 13  # Module.objects.count() + Scenario.objects.count()
    user_progress = UserModuleProgress.objects.filter(user=request.user)
    completed_modules_count = user_progress.filter(completed=True).count()
    completed_scenarios_count = UserScenarioProgress.objects.filter(user=request.user, completed=True).count()
    
    progress_percent = ((completed_modules_count + completed_scenarios_count) / total_items) * 100


    # Generate leaderboard entries with rank and level
    leaderboard = []
    for idx, user in enumerate(users_with_scores, start=1):
        completed = user.completed_modules
        if completed >= 8:
            level = "Expert"
        elif completed >= 5:
            level = "Advanced"
        elif completed >= 2:
            level = "Intermediate"
        else:
            level = "Beginner"

        leaderboard.append({
            'rank': idx,
            'user': user,
            'total_points': user.total_points or 0,
            'completed_modules': completed,
            'level': level
        })

    # Get current user's rank and points
    current_user_entry = next((entry for entry in leaderboard if entry['user'] == request.user), None)
    current_rank = current_user_entry['rank'] if current_user_entry else "-"
    your_points = current_user_entry['total_points'] if current_user_entry else 0

    # Find points to next rank (if any)
    higher_ranks = [entry for entry in leaderboard if entry['rank'] < current_rank]
    next_rank_points = (higher_ranks[-1]['total_points'] - your_points) if higher_ranks else 0

    context = {
        'leaderboard': leaderboard,
        'current_rank': current_rank,
        'next_rank_points': next_rank_points,
        'completed_scenarios': completed_scenarios_count,
        'progress_percent': int(progress_percent)
    }
    return render(request, 'leaderboard.html', context)

@login_required(login_url='login')
def profile(request):
    # Get all module progress for current user
    user_progress = UserModuleProgress.objects.filter(user=request.user)
    # Calculate total points (sum of all scores)
    total_points = user_progress.aggregate(total=models.Sum('score'))['total'] or 0
    # Count completed modules
    completed_modules = user_progress.filter(completed=True)
    completed_modules_count = user_progress.filter(completed=True).count()
    completed_scenarios_count = UserScenarioProgress.objects.filter(user=request.user, completed=True).count()
    achievement_count = UserAchievement.objects.filter(user=request.user).count()

    
    # Calculate the accuracy for each completed module
    module_accuracies = []
    for progress in completed_modules:
        accuracy = (progress.score / 100) * 100  # Assuming each module is worth 100 points
        module_accuracies.append(accuracy)

    # Calculate the average accuracy across all completed modules
    if module_accuracies:
        avg_accuracy = sum(module_accuracies) / len(module_accuracies)
    else:
        avg_accuracy = 0  # If no modules are completed

    # Capping the accuracy at 100%
    avg_accuracy = min(avg_accuracy, 100)


    # Total number of modules
    total_modules = Module.objects.count()
    
    # Determine level based on completed modules
    level = "Beginner"
    if completed_modules_count >= 8:
        level = "Expert"
    elif completed_modules_count >= 5:
        level = "Advanced"
    elif completed_modules_count >= 2:
        level = "Intermediate"
    
    context = {
        'user_progress': user_progress,
        'total_points': total_points,
        'completed_modules': completed_modules_count,
        'total_modules': total_modules,
        'level': level,
        'accuracy':avg_accuracy,
        'achievement_count': achievement_count,
        'completed_scenarios_count':completed_scenarios_count
    }
    return render(request, 'profile.html', context)

def burns_learning(request):
    return render(request, 'burns_learning.html')

@login_required
def burns_quiz(request):
    module = get_object_or_404(Module, slug='burns_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('burns_learning')
            else:
                return redirect('burns_quiz')
    else:
        form = QuizScoreForm(module_slug=module.slug)

        
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'burns_quiz.html', context)

def wounds_learning(request):
    return render(request, 'wounds_learning.html')

@login_required
def wounds_quiz(request):
    module = get_object_or_404(Module, slug='wounds_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('wounds_learning')
            else:
                return redirect('wounds_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)

        
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'wounds_quiz.html', context)

def fractures_learning(request):
    return render(request, 'fractures_and_sprains_learning.html')

@login_required
def fractures_and_sprains_quiz(request):
    module = get_object_or_404(Module, slug='fractures_and_sprains_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('fractures_and_sprains_learning')
            else:
                return redirect('fractures_and_sprains_quiz')
        
    else:
        form = QuizScoreForm(module_slug=module.slug)

        
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'fractures_and_sprains_quiz.html', context)

def cardiac_emergencies_learning(request):
    return render(request, 'cardiac_emergencies_learning.html')

@login_required
def cardiac_emergencies_quiz(request):
    module = get_object_or_404(Module, slug='cardiac_emergencies_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('cardiac_emergencies_learning')
            else:
                return redirect('cardiac_emergencies_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)
    
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'cardiac_emergencies_quiz.html', context)


def choking_learning(request):
    return render(request, 'choking_learning.html')

@login_required
def choking_quiz(request):
    module = get_object_or_404(Module, slug='choking_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('choking_learning')
            else:
                return redirect('choking_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)
    
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'choking_quiz.html', context)


def heat_learning(request):
    return render(request, 'heat_learning.html')

@login_required
def heat_quiz(request):
    module = get_object_or_404(Module, slug='heat_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('heat_learning')
            else:
                return redirect('heat_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)
    
    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'heat_quiz.html', context)


def cold_learning(request):
    return render(request, 'cold_learning.html')

@login_required
def cold_quiz(request):
    module = get_object_or_404(Module, slug='cold_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('cold_learning')
            else:
                return redirect('cold_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)


    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'cold_quiz.html', context)

def poison_learning(request):
    return render(request, 'poison_learning.html')

@login_required
def poison_quiz(request):
    
    module = get_object_or_404(Module, slug='poison_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('poison_learning')
            else:
                return redirect('poison_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)


    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'poison_quiz.html', context)

def venom_learning(request):
    return render(request, 'venom_learning.html')

@login_required
def venom_quiz(request):
    module = get_object_or_404(Module, slug='venom_quiz')
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('venom_learning')
            else:
                return redirect('venom_quiz')

    else:
        form = QuizScoreForm(module_slug=module.slug)


    context = {
        'module': module,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'venom_quiz.html', context)



def allergy_learning(request):
    return render(request, 'allergy_learning.html')

@login_required
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
                progress.completed =  progress.score >= module.passing_score
                progress.save()
                messages.success(request, "Your score has been updated!")
            else:
                progress.save()  # Save to increment attempts
                messages.info(request, "Your previous score was higher.")
                
            # Redirect back to the same page to show updated score
            if request.POST.get("action") == "back":
                return redirect('allergy_learning')
            else:
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

def RestrauntScenario(request):
    scenario = get_object_or_404(Scenario, slug='restaurant_scenario')
    progress, created = UserScenarioProgress.objects.get_or_create(
        user=request.user, 
        scenario=scenario
    )
    
    if request.method == 'POST':
        form = ScenarioScoreForm(request.POST)
        if form.is_valid():
            new_score = form.cleaned_data['score']
            # Get time_spent from POST, default to 0 if None or empty
            new_time_spent = form.cleaned_data.get('time_spent') or 0
            
            # Update attempts counter once per submission
            progress.attempts += 1
            
            # Only update score if new score is higher
            if new_score > progress.score:
                progress.score = new_score
                # Example passing score is 33
                progress.completed = progress.score >= 33
                progress.time_spent = new_time_spent
                progress.save()
                messages.success(request, f"Your score of {new_score} has been updated! " +
                                             ("You successfully completed the scenario!" if progress.completed else "Try again to improve your performance."))
            else:
                progress.save()  # Only update attempts
                messages.info(request, "Your score has been updated")
                
            if request.POST.get("action") == "back":
                return redirect('scenarios')
            else:
                return redirect('RestrauntScenario')
    else:
        form = ScenarioScoreForm(scenario_slug=scenario.slug)
    
    context = {
        'scenario': scenario,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'restraunt_scenario.html', context)

def HikingScenario(request):
    scenario = get_object_or_404(Scenario, slug='hiking_scenario')
    progress, created = UserScenarioProgress.objects.get_or_create(
        user=request.user, 
        scenario=scenario
    )
    
    if request.method == 'POST':
        form = ScenarioScoreForm(request.POST)
        if form.is_valid():
            new_score = form.cleaned_data['score']
            # Get time_spent from POST, default to 0 if None or empty
            new_time_spent = form.cleaned_data.get('time_spent') or 0
            
            # Update attempts counter once per submission
            progress.attempts += 1
            
            # Only update score if new score is higher
            if new_score > progress.score:
                progress.score = new_score
                # Example passing score is 33
                progress.completed = progress.score >= 33
                progress.time_spent = new_time_spent
                progress.save()
                messages.success(request, f"Your score of {new_score} has been updated! " +
                                             ("You successfully completed the scenario!" if progress.completed else "Try again to improve your performance."))
            else:
                progress.save()  # Only update attempts
                messages.info(request, "Your score has been updated")
                
            if request.POST.get("action") == "back":
                return redirect('scenarios')
            else:
                return redirect('HikingScenario')
    else:
        form = ScenarioScoreForm(scenario_slug=scenario.slug)
    
    context = {
        'scenario': scenario,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }
    return render(request, 'hiking_scenario.html', context)

@login_required
def BurnsScenario(request):
    scenario = get_object_or_404(Scenario, slug='burns_scenario')
    progress, created = UserScenarioProgress.objects.get_or_create(
        user=request.user, 
        scenario=scenario
    )
    
    if request.method == 'POST':
        form = ScenarioScoreForm(request.POST)
        if form.is_valid():
            new_score = form.cleaned_data['score']
            # Get time_spent from POST, default to 0 if None or empty
            new_time_spent = form.cleaned_data.get('time_spent') or 0
            
            # Update attempts counter once per submission
            progress.attempts += 1
            
            # Only update score if new score is higher
            if new_score > progress.score:
                progress.score = new_score
                # Example passing score is 33
                progress.completed = progress.score >= 33
                progress.time_spent = new_time_spent
                progress.save()
                messages.success(request, f"Your score of {new_score} has been updated! " +
                                             ("You successfully completed the scenario!" if progress.completed else "Try again to improve your performance."))
            else:
                progress.save()  # Only update attempts
                if progress.attempts>1:
                    messages.info(request, "Your previous score was higher.")
                else:
                    messages.info(request, "Your score has been updated")
            if request.POST.get("action") == "back":
                return redirect('scenarios')
            else:
                return redirect('BurnsScenario')
    else:
        form = ScenarioScoreForm(scenario_slug=scenario.slug)
    
    context = {
        'scenario': scenario,
        'current_score': progress.score,
        'completed': progress.completed,
        'attempts': progress.attempts,
        'form': form
    }

    return render(request, 'burns_scenario.html', context)

