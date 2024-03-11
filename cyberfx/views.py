from django.shortcuts import render, redirect
from .models import ExpertAdvisor, Review
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import os, json

def index(request):
    return render(request, 'cyberfx/index.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login_function')  # Redirect to a success page
        else:
            # Handle invalid login
            return render(request, 'cyberfx/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'cyberfx/login.html')

def advisors(request):
    advisors = ExpertAdvisor.objects.all()
    return render(request, 'cyberfx/advisor_list.html', {'advisors' : advisors})

def search_category(request, category):
    advisors = ExpertAdvisor.objects.filter(category=category) 
    results = list(advisors.values('id', 'ea_name', 'personal_review', 'last_updated', 'category'))  
    return JsonResponse(results, safe=False)

def search_advisors(request):
    search_term = request.GET.get('term', '') 
    results = ExpertAdvisor.objects.filter(
        Q(ea_name__icontains=search_term)
    ) 
    results = results[:10] 
    data = list(results.values('id', 'ea_name', 'personal_review', 'last_updated')) 

    return JsonResponse(data, safe=False) 

@login_required
def advisor_info(request, id):
    advisor = ExpertAdvisor.objects.get(id=id)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                user = request.user
                comment = request.POST['comment']
                print(comment)
#                review.save(advisor=advisor, user=user, comment=comment, approved=True)
                return redirect('login_function')
        else:
            if request.method == 'POST':
                comment = request.POST['comment']
                user = request.user
                review = Review(advisor=advisor, user=user, comment=comment, approved=False)
                review.save()
                return redirect('login_function')
    
    review = Review.objects.filter(advisor=advisor, approved=True)
    username = request.user.username
    return render(request, 'cyberfx/advisor_info.html', {'advisor': advisor, 'reviews': review, 'username': username})

def login_function(request):
    if request.user.is_authenticated:
        reviews = Review.objects.select_related('advisor', 'user').filter(user=request.user)
        all_reviews = Review.objects.select_related('advisor', 'user').filter(approved=False)
        username = request.user.username
        print(reviews)
        if request.user.is_superuser:
            return render(request, 'cyberfx/admin_panel.html', {'reviews' : all_reviews })
        else:
            return render(request, 'cyberfx/user_panel.html', {'reviews' : reviews, 'username' : username})

    else:
        return redirect('login')