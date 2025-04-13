# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # e.g., 'allergy_quiz'
    max_score = models.PositiveIntegerField(default=50)  # Default based on your quiz
    passing_score = models.PositiveIntegerField(default=60)  # Minimum to be considered complete
    
    def __str__(self):
        return self.title

class UserModuleProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'module')
    
    def __str__(self):
        return f"{self.user.username} - {self.module.title} ({self.score})"