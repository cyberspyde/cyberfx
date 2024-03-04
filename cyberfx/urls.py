from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('advisors/', views.advisor_list, name='advisor_list'),
    # path('api/new_customer', views.new_customer, name='new_customer'),
    # path('api/customer_detail/<int:ticket_number>', views.CustomerViewAPIView.as_view()),
    # path('api/latestcustomers', views.LatestCustomers.as_view()),
    # path('api/generatepdf/<int:ticket_number>', views.generatePDF),
    # path('api/process_data/<int:ticket_number>', views.process_data)
]