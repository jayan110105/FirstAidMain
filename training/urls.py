from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('modules/', views.modules, name='modules'),
    path('scenarios/', views.scenarios, name='scenarios'),
    path('achievements/', views.achievements, name='achievements'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('burns-learning/', views.burns_learning, name='burns_learning'),
    path('burns-quiz/', views.burns_quiz, name='burns_quiz'),
    path('wounds-learning/', views.wounds_learning, name='wounds_learning'),
    path('wounds-quiz/', views.wounds_quiz, name='wounds_quiz'),
    path('fractures-learning/', views.fractures_learning, name='fractures_learning'),
    path('fractures-quiz/', views.fractures_and_sprains_quiz, name='fractures_and_sprains_quiz'),
    path('cardiac-emergencies-learning/', views.cardiac_emergencies_learning, name='cardiac_emergencies_learning'),
    path('cardiac-emergencies-quiz/', views.cardiac_emergencies_quiz, name='cardiac_emergencies_quiz'),
    path('choking-learning/', views.choking_learning, name='choking_learning'),
    path('choking-quiz/', views.choking_quiz, name='choking_quiz'),
    path('heat-learning/', views.heat_learning, name='heat_learning'),
    path('heat-quiz/', views.heat_quiz, name='heat_quiz'),
    path('cold-learning/', views.cold_learning, name='cold_learning'),
    path('cold-quiz/', views.cold_quiz, name='cold_quiz'),
    path('poison-learning/', views.poison_learning, name='poison_learning'),
    path('poison-quiz/', views.poison_quiz, name='poison_quiz'),
    path('venom-learning/', views.venom_learning, name='venom_learning'),
    path('venom-quiz/', views.venom_quiz, name='venom_quiz'),
    path('allergy-learning/', views.allergy_learning, name='allergy_learning'),
    path('allergy-quiz/', views.allergy_quiz, name='allergy_quiz'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('restraunt-scenario/', views.RestrauntScenario, name='RestrauntScenario'),
    path('hiking-scenario/', views.HikingScenario, name='HikingScenario'),
    path('burns-scenario/', views.BurnsScenario, name='BurnsScenario'),
]
