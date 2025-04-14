from django.contrib import admin
from .models import Module,UserModuleProgress, Scenario, UserScenarioProgress

# Register your models here.
admin.site.register(Module)
admin.site.register(UserModuleProgress)
admin.site.register(Scenario)
admin.site.register(UserScenarioProgress)