from django.contrib import admin
from .models import Module,UserModuleProgress,Achievement,UserAchievement

# Register your models here.
admin.site.register(Module)
admin.site.register(UserModuleProgress)
admin.site.register(Achievement)
admin.site.register(UserAchievement)