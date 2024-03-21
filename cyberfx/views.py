from django.shortcuts import render, redirect
from .models import ExpertAdvisor, Review
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
import os, re, subprocess
from django.conf import settings
from django.http import HttpResponse, Http404

uploads_base_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1 MB
ALLOWED_FORMATS = ('png', 'jpeg', 'jpg', 'bmp', 'heic', 'heif')
MAX_ZIP_SIZE = 5 * 1024 * 1024  # 5 MB

def handle_images(request, ea_folder):
        images = request.FILES.getlist('images')
        if len(images) > 3:
            messages.error(request, 'You can only upload a maximum of 3 images')
            if id is not None:
                return 'error'
            else:
                return 'error'

        for image in images:
            if image.size > MAX_IMAGE_SIZE:
                messages.error(request, 'Images cannot exceed 1MB each')
                return 'error'
            
        for image in images:
            filename, extension = os.path.splitext(image.name.lower())
            if extension[1:] not in ALLOWED_FORMATS:  
                messages.error(request, 'Only .png, .jpeg, .jpg, .bmp, .heic, .heif files are allowed')
                return 'error' 

            image_path = os.path.join(ea_folder, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

def handle_zip(request, ea_folder):
        zip_file = request.FILES.get('zip_file')
        if zip_file:  
            if not zip_file.name.endswith('.zip'):
                messages.error(request, 'Only .zip files are allowed')
                return 'error'

            if zip_file.size > MAX_ZIP_SIZE:
                messages.error(request, 'Zip file cannot exceed 5MB')
                return 'error'

            zip_path = os.path.join(ea_folder, zip_file.name)
            with open(zip_path, 'wb+') as destination:
                for chunk in zip_file.chunks():
                    destination.write(chunk)

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
            return redirect('login_function')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'cyberfx/login.html')

def advisors(request):
    advisors = ExpertAdvisor.objects.filter(approved=True).exclude(personal_review='').order_by('-last_updated')
    return render(request, 'cyberfx/advisor_list.html', {'advisors' : advisors})

def search_category(request, category):
    advisors = ExpertAdvisor.objects.filter(category=category, approved=True).exclude(personal_review='').order_by('-last_updated')
    results = list(advisors.values('id', 'ea_name', 'personal_review', 'last_updated', 'category'))  
    return JsonResponse(results, safe=False)

def search_advisors(request):
    search_term = request.GET.get('term', '') 
    results = ExpertAdvisor.objects.filter(
        Q(ea_name__icontains=search_term)
    ) 
    results = results[:10] 
    data = list(results.values('id', 'ea_name', 'personal_review', 'last_updated', 'category')) 
    return JsonResponse(data, safe=False) 

@login_required
def advisor_info(request, id):
    advisor = ExpertAdvisor.objects.get(id=id)
    user = request.user
    review_count = Review.objects.filter(
        advisor=advisor, user=request.user
    ).count()

    if request.user.is_superuser:
        if request.method == 'POST':
            comment = request.POST['comment']
            ea_name_filtered = clean_text(advisor.ea_name.lower())
            ea_folder = os.path.join(uploads_base_dir, ea_name_filtered)
            if not os.path.exists(ea_folder):
                os.makedirs(ea_folder)
            if comment == '':
                messages.error(request, 'Please provide a review')

            images = request.FILES.getlist('images')
            if len(images) > 3:
                messages.error(request, 'You can only upload a maximum of 3 images')
            for image in images:
                filename, extension = os.path.splitext(image.name.lower())
                if extension[1:] not in ALLOWED_FORMATS:  
                    messages.error(request, 'Only .png, .jpeg, .jpg, .bmp, .heic, .heif files are allowed')

                if image.size > MAX_IMAGE_SIZE:
                    messages.error(request, 'Images cannot exceed 1MB each')
                
            zip_file = request.FILES.get('zip_file')
            if zip_file:  
                if not zip_file.name.endswith('.zip'):
                    messages.error(request, 'Only .zip files are allowed')

                if zip_file.size > MAX_ZIP_SIZE:
                    messages.error(request, 'Zip file cannot exceed 5MB')

            if messages.get_messages(request):
                return redirect('advisor_info', id=id)

            for image in images:   
                image_path = os.path.join(ea_folder, image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
            if zip_file:
                zip_path = os.path.join(ea_folder, zip_file.name)
                with open(zip_path, 'wb+') as destination:
                    for chunk in zip_file.chunks():
                        destination.write(chunk)


            review = Review(advisor=advisor, user=user, comment=comment, approved=True)
            review.save()    
        review = Review.objects.filter(advisor=advisor, approved=True)
        username = request.user.username
        return render(request, 'cyberfx/advisor_info.html', {'advisor': advisor, 'reviews': review, 'username': username, 'admin' : True})
    else:
        if request.method == 'POST':
            if review_count >= 5:
                messages.error(request, 'You have reached the maximum number of reviews for this advisor')
                return redirect('advisors')
            comment = request.POST['comment']
            review = Review(advisor=advisor, user=user, comment=comment, approved=False)
            review.save()
            return redirect('login_function')
        review = Review.objects.filter(advisor=advisor, approved=True)
        username = request.user.username
        return render(request, 'cyberfx/advisor_info.html', {'advisor': advisor, 'reviews': review, 'username': username, 'admin' : False})


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
        ea_name = request.POST['advisor']
        ea_name_filtered = clean_text(ea_name.lower())
        category = request.POST['category']
        personal_review = request.POST['review']
        created_by = request.user
        images = request.FILES.getlist('images')
        if personal_review == '':
            messages.error(request, 'Please provide a review')
            return redirect('add_advisor')

        ea_folder = os.path.join(uploads_base_dir, ea_name_filtered)
        print(ea_folder)
        if not os.path.exists(ea_folder):
            os.makedirs(ea_folder)

            # Handle Images
            images = request.FILES.getlist('images')
            if len(images) > 3:
                messages.error(request, 'You can only upload a maximum of 3 images')
                return redirect('add_advisor')

            for image in images:
                if image.size > MAX_IMAGE_SIZE:
                    messages.error(request, 'Images cannot exceed 1MB each')
                    return redirect('add_advisor')
                
            for image in images:
                filename, extension = os.path.splitext(image.name.lower())
                if extension[1:] not in ALLOWED_FORMATS:  
                    messages.error(request, 'Only .png, .jpeg, .jpg, .bmp, .heic, .heif files are allowed')
                    return redirect('add_advisor') 

                image_path = os.path.join(ea_folder, image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            # Handle Zip file
            zip_file = request.FILES.get('zip_file')
            if zip_file:  
                if not zip_file.name.endswith('.zip'):
                    messages.error(request, 'Only .zip files are allowed')
                    return redirect('add_advisor')

                if zip_file.size > MAX_ZIP_SIZE:
                    messages.error(request, 'Zip file cannot exceed 5MB')
                    return redirect('add_advisor')

                zip_path = os.path.join(ea_folder, zip_file.name)
                with open(zip_path, 'wb+') as destination:
                    for chunk in zip_file.chunks():
                        destination.write(chunk)

        if request.user.is_superuser:
            advisor = ExpertAdvisor(ea_name=ea_name, personal_review=personal_review, category=category, created_by=created_by, approved=True)
            advisor.save()
            return redirect('advisors')
        else:
            advisor = ExpertAdvisor(ea_name=ea_name, personal_review=personal_review, category=category, created_by=created_by)
            advisor.save()
            return redirect('login_function')
    else:
        return render(request, 'cyberfx/add_advisor.html', {'username' : request.user.username})

def download(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404