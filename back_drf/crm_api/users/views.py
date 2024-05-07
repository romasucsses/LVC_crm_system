from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import Administrator
from .models import User
from .serializers import UserSerializer


class ListUsersAPIView(APIView):
    permission_classes = [Administrator]

    def get(self, request):
        users = User.objects.all()
        serialized_info = UserSerializer(users, many=True)
        return Response(serialized_info.data)

    def post(self, request):
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            new_user.save(is_active=False)
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
        serialized_info = UserSerializer(self.get_user(pk))
        return Response(serialized_info.data)

    def patch(self, request, pk):
        serialized_info = UserSerializer(self.get_user(pk), data=request.data, partial=True)
        if serialized_info.is_valid():
            serialized_info.save()
            return Response('Edited Successfully')
        return Response('Is Fail')

    def delete(self, request, pk):
        self.get_user(pk).delete()
        return Response("User have successfully removed")


class AddNewUserAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        new_user = UserSerializer(User, data=request.data)
        if new_user.is_valid():
            new_user.save()
            return Response("New User was successfully added")
        return Response("Was failed in adding new user")
