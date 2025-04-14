from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Module(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    max_score = models.PositiveIntegerField(default=50)
    passing_score = models.PositiveIntegerField(default=60)
    
    def __str__(self):
        return self.title


class UserModuleProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    #time_spent = models.DurationField(default=timedelta()) 
    time_spent = models.IntegerField(default=100)  # Needed for "Quick Thinker" achievement

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.username} - {self.module.title} ({self.score})"


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="CSS class or image name for the achievement icon")

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"