from django.shortcuts import render, redirect
from .models import ExpertAdvisor, Review
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import os, re
from django.conf import settings

def clean_text(text, replace_with=''):
    return re.sub(r"[^\w\s]|\s+", replace_with, text).strip() 

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
    advisors = ExpertAdvisor.objects.filter(approved=True).order_by('-last_updated')[:25]
    return render(request, 'cyberfx/advisor_list.html', {'advisors' : advisors})

def search_category(request, category):
    advisors = ExpertAdvisor.objects.filter(category=category, approved=True).order_by('-last_updated')[:10]
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
    user = request.user

    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                user = request.user
                comment = request.POST['comment']
                review = Review(advisor=advisor, user=user, comment=comment, approved=True)
                review.save()
        else:
            if request.method == 'POST':
                comment = request.POST['comment']
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
        all_advisors = ExpertAdvisor.objects.filter(approved=False)
        advisors = ExpertAdvisor.objects.filter(created_by=request.user).order_by('-last_updated')
        username = request.user.username
        if request.user.is_superuser:
            return render(request, 'cyberfx/admin_panel.html', {'reviews' : all_reviews, 'advisors' : all_advisors})
        else:
            return render(request, 'cyberfx/user_panel.html', {'reviews' : reviews, 'username' : username, 'advisors' : advisors})

    else:
        return redirect('login')
    
def approve_review(request, id):
    review = Review.objects.select_related('advisor').filter(id=id)
    
    for r in review:
        r.advisor.last_updated = timezone.now()
        r.advisor.save()
        r.approved = True
        r.save()
    return redirect('login_function')

def approve_advisor(request, id):
    advisor = ExpertAdvisor.objects.get(id=id)
    advisor.approved = True
    advisor.save()
    return redirect('login_function')

def reject_advisor(request, id):
    advisor = ExpertAdvisor.objects.get(id=id)
    advisor.delete()
    return redirect('login_function')

def reject_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('login_function')

def approve_all_advisors(request):
    advisors = ExpertAdvisor.objects.filter(approved=False)
    for advisor in advisors:
        advisor.approved = True
        advisor.save()
    return redirect('login_function')

def approve_all_reviews(request):
    reviews = Review.objects.filter(approved=False)
    for review in reviews:
        review.approved = True
        review.save()
    return redirect('login_function')

def reject_all_advisors(request):
    advisors = ExpertAdvisor.objects.filter(approved=False)
    for advisor in advisors:
        advisor.delete()
    return redirect('login_function')

def reject_all_reviews(request):
    reviews = Review.objects.filter(approved=False)
    for review in reviews:
        review.delete()
    return redirect('login_function')

def add_advisor(request):
    if request.method == 'POST':
        ea_name = clean_text(request.POST['advisor'].lower())
        category = request.POST['category']
        personal_review = request.POST['review']
        created_by = request.user
        images = request.FILES.getlist('images')
        print(category)
        if len(images) > 3:
            
            return render(request, 'cyberfx/add_advisor.html', {'error_message': 'Maximum of 3 images allowed'})

        MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1 MB

        for image in images:
            if image.size > MAX_IMAGE_SIZE:
                return render(request, 'cyberfx/add_advisor.html', {'error_message': 'Images cannot exceed 1MB'})

        uploads_base_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

        ea_folder = os.path.join(uploads_base_dir, ea_name)
        if not os.path.exists(ea_folder):
            os.makedirs(ea_folder)  # Create the folder if needed

        # Handle images
        for image in request.FILES.getlist('images'):
            image_path = os.path.join(ea_folder, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)


        # Process uploaded zip file (max 1)
        zip_file = request.FILES.get('zip_file')
        if zip_file:  
            if not zip_file.name.endswith('.zip'):
                print("File type: ", zip_file.name.split('.')[-1])
                return render(request, 'cyberfx/add_advisor.html', {'error_message': 'Only .zip files are allowed'})

            # Size validation (in bytes)
            MAX_ZIP_SIZE = 5 * 1024 * 1024  # 5 MB
            if zip_file.size > MAX_ZIP_SIZE:
                print("File size: ", zip_file.size)
                return render(request, 'cyberfx/add_advisor.html', {'error_message': 'Zip file cannot exceed 5MB'})

            zip_path = os.path.join(ea_folder, zip_file.name)
            with open(zip_path, 'wb+') as destination:
                for chunk in zip_file.chunks():
                    destination.write(chunk)

        advisor = ExpertAdvisor(ea_name=ea_name, personal_review=personal_review, category=category, created_by=created_by)
        advisor.save()
        return redirect('advisors')
    else:
        return render(request, 'cyberfx/add_advisor.html')

