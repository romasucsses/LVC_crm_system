from django.urls import path
from .views import *


urlpatterns = [
    path('list-customers/', ListCustomersAPIView.as_view(), name="list_of_customers"),
    path('detail-view/customer/<int:pk>/', DetailCustomerAPIView.as_view(), name="detail_customer_view"),
    path('add-new-customer/', AddNewCustomerAPIView.as_view(), name="add_new_customer"),
    path('update-customer/<int:pk_customer>/', UpdateCustomerAPIView.as_view(), name='update_customer')

]
