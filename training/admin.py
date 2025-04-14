from django.contrib import admin
from .models import Module,UserModuleProgress, Scenario, UserScenarioProgress, Achievement,UserAchievement

# Register your models here.

admin.site.register(Scenario)
admin.site.register(UserScenarioProgress)

admin.site.register(Achievement)
admin.site.register(UserAchievement)

admin.site.register(Module)
admin.site.register(UserModuleProgress)