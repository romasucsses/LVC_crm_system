from django.urls import path
from .views import *

urlpatterns = [
    path('orders-list/', ListOrdersAPIView.as_view(), name='orders_list'),
    path('detail-order/<int:pk>/', DetailOrderAPIView.as_view(), name='detail_order'),
    path('create-order/', CreateOrderAPIView.as_view(), name='create_order'),
    # invoices
    path('invoices-list/', ListInvoicesAPIView.as_view(), name='invoices_list'),
    path('detail-invoice/<int:pk>/', DetailInvoiceAPIView.as_view(), name='detail_invoice'),
    path('generate_pdf/', GenerateInvoice.as_view())
]
