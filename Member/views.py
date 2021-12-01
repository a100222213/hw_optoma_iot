
from django.forms import ValidationError
from django.http import JsonResponse
from django.db import transaction
from rest_framework import viewsets

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from iot.helper import PayloadHandler

from .models import Member
from .serializers import MemberSerializer


# Create your views here.
class MemberView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def payload(self, msg, _data):

        return_code, return_message = PayloadHandler.get_return_code_n_message(
            msg=msg)

        payload = PayloadHandler.set_payload(
            data=_data,
            return_code=return_code,
            return_message=return_message
        )
        return payload

    @swagger_auto_schema(
        operation_summary='會員註冊',
        operation_description='會員註冊API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            properties={
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='電子郵件'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='行動電話'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='會員姓名'),
                'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='生日'),
                'gender': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='性別'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='地址'),
                'oauthid': openapi.Schema(type=openapi.TYPE_STRING, description='認證ID'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='會員密碼')
            }
        )
    )
    def create(self, request):
        """[Member Create]

        Args:
            request ([object]): []

        Returns:
            [JsonResponse]: [serializer]
        """
        data = {
            **request.data,
        }
        serializer = self.serializer_class(data=request.data)
        try:
            # 利用DB原子性
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                serializer.save()
            msg = 'success'

        except ValidationError as error:
            msg = error.messages

        payload = self.payload(msg, data)

        return JsonResponse(payload)

    @swagger_auto_schema(
        operation_summary='會員資料修改',
        operation_description='會員資料修改API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            properties={
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='電子郵件'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='行動電話'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='會員姓名'),
                'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='生日'),
                'gender': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='性別'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='地址'),
                'oauthid': openapi.Schema(type=openapi.TYPE_STRING, description='認證ID'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='會員密碼')
            }
        )
    )
    def partial_update(self, request, _email=None):
        if not self.get_queryset().filter(email=_email).exists():
            msg = 'email {} is not exists.'.format(_email)
        else:
            email = self.get_queryset().get(email=_email)
            data = request.data
            serializer = self.serializer_class(
                email, data=data, partial=True)
            try:
                # 利用DB原子性
                with transaction.atomic():
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                msg = 'success'
            except ValidationError as error:
                msg = error.message

            payload = self.payload(msg, request.data)

            return JsonResponse(payload)
