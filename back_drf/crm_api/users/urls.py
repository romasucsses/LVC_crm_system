from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    path('get-token/', TokenObtainPairView().as_view(), name='token_obtain_pair'),
    path('get-refresh-token/', TokenRefreshView().as_view(), name='token_refresh'),
    path('users-list/', ListUsersAPIView.as_view(), name='user_list'),
    path('detail/user/<int:pk>/', UserDetailAPIView.as_view(), name='detail_user'),
    path('add-new-user/', AddNewUserAPIView.as_view(), name='add_new_user')
]
