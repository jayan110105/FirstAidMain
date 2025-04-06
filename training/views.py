from django.shortcuts import render

def modules(request):
    return render(request, 'modules.html')

def scenarios(request):
    return render(request, 'scenarios.html')

def achievements(request):
    return render(request, 'achievements.html')

def leaderboard(request):
    return render(request, 'leaderboard.html')

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
