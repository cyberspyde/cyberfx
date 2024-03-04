from django.shortcuts import render, redirect
from .models import ExpertAdvisor, Review
from django.contrib.auth.decorators import login_required
import os, json

def index(request):
    return render(request, 'cyberfx/index.html')

def advisor_list(request):
    advisors = ExpertAdvisor.objects.all()
    return render(request, 'cyberfx/advisor_list.html', {'advisors' : advisors})

def advisor_detail(request, pk):
    advisor = ExpertAdvisor.objects.get(pk=pk)
    reviews = Review.objects.filter(advisor=advisor, approved=True)
    return render(request, 'advisors/detail.html', {'advisor': advisor, 'reviews': reviews})

@login_required
def add_review(request, pk):
    # ... form handling for creating a new Review (approve=False by default)
    return redirect('advisor_detail', pk=pk) 
