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
    # path('api/new_customer', views.new_customer, name='new_customer'),
    # path('api/customer_detail/<int:ticket_number>', views.CustomerViewAPIView.as_view()),
    # path('api/latestcustomers', views.LatestCustomers.as_view()),
    # path('api/generatepdf/<int:ticket_number>', views.generatePDF),
    # path('api/process_data/<int:ticket_number>', views.process_data)
]