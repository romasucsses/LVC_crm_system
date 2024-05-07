from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_client", False)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_client", False)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=155, unique=True, null=False)
    password = models.CharField(max_length=355)
    first_name = models.CharField(max_length=55, null=True)
    last_name = models.CharField(max_length=55, null=True)

    is_active = models.BooleanField(default=True)
    is_client = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'user{self.username}'
