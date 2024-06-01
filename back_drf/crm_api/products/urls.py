from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'beverage', BeverageViewSet)
router.register(r'states', StateViewSet)
router.register(r'stock-product', StockProductViewSet)
router.register(r'code-product', CodeProductViewSet)
router.register(r'price-product', PriceProductViewSet)


urlpatterns = [
    path('list-products-without-price/', ListProductsWithoutPriceAPIView.as_view(), name='products_without_price'),
    path('list-products-with-price/', ListProductsWithPriceAPIView.as_view(), name='products_with_price'),
    path('admin-manage-products/', AddNewProductAPIView.as_view(), name='manage_products'),
    path('admin-manage-detail-product/', ManageDetailProductAPIView.as_view(), name='manage_detail_product'),
    path('products-router/', include(router.urls))
]
