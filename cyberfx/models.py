from django.db import models
from django.contrib.auth.models import User  # For user reviews

class ExpertAdvisor(models.Model):
    CATEGORY_CHOICES = (
            ('Trash', 'Trash'),
            ('Testing', 'Testing'),
            ('Goodfornow', 'Goodfornow'),
        )
    
    ea_name = models.CharField(max_length=100)
    personal_review = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Trash')
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Review(models.Model):
    advisor = models.ForeignKey(ExpertAdvisor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    posted_date = models.DateTimeField(auto_now=True)