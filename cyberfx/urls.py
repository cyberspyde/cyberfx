from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cyberfx/advisors/', views.advisors, name='advisors'),
    path('cyberfx/search-advisors/', views.search_advisors, name='search_advisors'),
    path('cyberfx/search-category/<str:category>', views.search_category, name='search_category'),
    path('cyberfx/advisor-info/<int:id>', views.advisor_info, name='advisor_info'),
    path('cyberfx/login_function/', views.login_function, name='login_function'),
    path('cyberfx/login/', views.login_view, name='login'),
    path('cyberfx/logout/', views.logout_view, name='logout'),
    path('cyberfx/approve-review/<int:id>', views.approve_review, name='approve_review'),
    path('cyberfx/reject-review/<int:id>', views.reject_review, name='reject_review'),
    path('cyberfx/approve-all-reviews/', views.approve_all_reviews, name='approve_all_reviews'),
    path('cyberfx/reject-all-reviews/', views.reject_all_reviews, name='reject_all_reviews'),
]