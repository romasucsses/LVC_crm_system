from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import Administrator
from .models import User
from .serializers import UserSerializer
from utils.cache_logic import *


class ListUsersAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        result = get_set_cache(
            queryset=User.objects.all(),
            serializer=UserSerializer,
            cache_name=USERS_LIST_CACHE_NAME,
            type_data='list'
        )
        return Response(result)

    def post(self, request):
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            new_user.save(is_active=False)
            cache.delete(USERS_LIST_CACHE_NAME)
            cache.delete(USER_DETAIL_CACHE_NAME)
            return Response("New user was add successfully")


class UserDetailAPIView(APIView):
    permission_classes = [Administrator]

    def get_user(self, pk):
        global user
        try:
            user = User.objects.get(pk=pk)
            return user
        except user.DoesNotExist:
            raise ObjectDoesNotExist("user is not found")

    def get(self, request, pk):
        result = get_set_cache(
            queryset=self.get_user(pk),
            serializer=UserSerializer,
            cache_name=USER_DETAIL_CACHE_NAME,
            type_data='detail'
        )
        return Response(result)

    def patch(self, request, pk):
        serialized_info = UserSerializer(self.get_user(pk), data=request.data, partial=True)
        if serialized_info.is_valid():
            serialized_info.save()
            cache.delete(USERS_LIST_CACHE_NAME)
            cache.delete(USER_DETAIL_CACHE_NAME)
            return Response('Edited Successfully')
        return Response('Is Fail')

    def delete(self, request, pk):
        self.get_user(pk).delete()
        cache.delete(USERS_LIST_CACHE_NAME)
        cache.delete(USER_DETAIL_CACHE_NAME)
        return Response("User have successfully removed")


class AddNewUserAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_user = UserSerializer(User, data=request.data)
        if new_user.is_valid():
            new_user.save()
            cache.delete(USERS_LIST_CACHE_NAME)
            return Response("New User was successfully added")
        return Response("Was failed in adding new user")
