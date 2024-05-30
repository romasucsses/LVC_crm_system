from django.urls import path
from .views import *

urlpatterns = [
    path('send-email/', SendEmailAPIView.as_view(), name="send_email")
]
