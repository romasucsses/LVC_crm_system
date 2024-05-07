from django.urls import path
from .views import *

urlpatterns = [
    path('list-products-without-price/', ListProductsWithoutPriceAPIView.as_view(), name='products_without_price'),
    path('list-products-with-price/', ListProductsWithPriceAPIView.as_view(), name='products_with_price'),
    path('admin-manage-products/', ManageListProductsAPIView.as_view(), name='manage_products'),
    path('admin-manage-detail-product/', ManageDetailProductAPIView.as_view(), name='manage_detail_product')

]
