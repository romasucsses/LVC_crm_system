from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *
from .tasks import send_emails
from users.permissions import Administrator


class SendEmailAPIView(APIView):
    permission_classes = [Administrator]

    def post(self, request):
        emails_list = request.data.get("emails")
        title = request.data.get("title")
        msg = request.data.get("msg")
        file = request.FILES.get('file')

        file_path = None
        if file is not None:
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            file_path = default_storage.path(file_name)

        send_emails.delay(emails_list=emails_list, title=title, msg=msg, file_path=file_path)
        return Response("the task is started")
