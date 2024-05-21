from django.urls import path
from .views import *
from email_sender.views import SendEmailAPIView

urlpatterns = [
    path('list-customers/', ListCustomersAPIView.as_view(), name="list_of_customers"),
    path('detail-view/customer/<int:pk>/', DetailCustomerAPIView.as_view(), name="detail_customer_view"),
    path('add-new-customer/', AddNewCustomerAPIView.as_view(), name="add_new_customer"),
    path('send-email-to-customers/', SendEmailAPIView.as_view(), name="send_email_to_customer")
]
