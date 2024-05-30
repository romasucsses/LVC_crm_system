from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/customers/', include('customers.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/email/', include('email_sender.urls'))
]
