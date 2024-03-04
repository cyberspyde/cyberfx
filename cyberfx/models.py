from django.db import models
from django.contrib.auth.models import User  # For user reviews

class ExpertAdvisor(models.Model):

    number = models.CharField(max_length=10, null=True, blank=True)  # Assuming "#" is a string
    ea_name = models.CharField(max_length=100)
    personal_review = models.TextField(null=True, blank=True)
    lessons_learned = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  

class Review(models.Model):
    advisor = models.ForeignKey(ExpertAdvisor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
