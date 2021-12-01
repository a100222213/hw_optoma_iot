# Create your views here.
from django.forms import ValidationError
from django.http import JsonResponse
from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import DeviceSerializer
from . import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from iot.helper import PayloadHandler


class DeviceView(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.AllowAny,)

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
        operation_summary='設備清單查詢API',
        manual_parameters=[
            openapi.Parameter(
                name='switch',
                in_=openapi.IN_QUERY,
                description='分頁開關',
                default=True,
                type=openapi.TYPE_BOOLEAN,
                required=True
            ),
            openapi.Parameter(
                name='serialnumber',
                in_=openapi.IN_QUERY,
                description='設備序列號',
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def retrieve(self, request):
        """
        Return a list of phoneclass.
        """
        pagenation = True

        instances = self.filter_queryset(
            self.get_queryset())
        msg = 'success'

        if request.query_params.get('switch', None) == 'true':
            pagenation = True
        else:
            pagenation = False

        if pagenation:
            page = self.paginate_queryset(instances)

            serializer = self.get_serializer(page, many=True)

            _data = serializer.data

            _page = self.get_paginated_response(_data)

            payload = self.payload(msg, _data)
            payload['previous'] = _page.data['previous']
            payload['next'] = _page.data['next']
            payload['count'] = _page.data['count']

        else:
            serializer = self.get_serializer(instances, many=True)

            _data = serializer.data

            payload = self.payload(msg, _data)

        return JsonResponse(payload)

    @swagger_auto_schema(
        operation_summary='設備綁定(bind=1)/解綁定(bind=0)',
        operation_description='設備綁定/解綁定API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            properties={
                'serialnumber': openapi.Schema(type=openapi.TYPE_STRING, description='裝置序列號'),
                'model': openapi.Schema(type=openapi.TYPE_STRING, description='裝置型號'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='裝置名稱'),
                'bind': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='裝置綁定狀態')
            }
        )
    )
    def create(self, request):
        """[Device Create]

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
        operation_summary='設備相關資料修改',
        operation_description='設備相關資料修改API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,

            properties={
                'serialnumber': openapi.Schema(type=openapi.TYPE_STRING, description='裝置序列號'),
                'model': openapi.Schema(type=openapi.TYPE_STRING, description='裝置型號'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='裝置名稱'),
                'bind': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='裝置綁定狀態')
            }
        )
    )
    def partial_update(self, request, _serialnumber=None):
        if not self.get_queryset().filter(serialnumber=_serialnumber).exists():
            msg = 'serialnumber {} is not exists.'.format(_serialnumber)
        else:
            serialnumber = self.get_queryset().get(serialnumber=_serialnumber)
            data = request.data
            serializer = self.serializer_class(
                serialnumber, data=data, partial=True)
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
