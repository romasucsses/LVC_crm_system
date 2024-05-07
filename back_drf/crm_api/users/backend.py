from .models import User
from django.contrib.auth.backends import ModelBackend


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, is_active=False):

        global user
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                return user

        except user.DoesNotExist:
            return None
