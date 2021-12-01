"""iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Member.views import MemberView
from Device.views import DeviceView


urlpatterns_api = [
    #path('admin/', admin.site.urls),
    path('api/', include([
        path('refresh-token', refresh_jwt_token),
        path('member/register',
             MemberView.as_view({'post': 'create'})),
        path('member/<str:_email>',
             MemberView.as_view({'post': 'partial_update'})),
        path('device/bind',
             DeviceView.as_view({'post': 'create'})),
        path('device/<str:_serialnumber>',
             DeviceView.as_view({'patch': 'partial_update'})),
        path('device',
             DeviceView.as_view({'get': 'retrieve'})),
    ])),
]

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1'
    ),
    patterns=urlpatterns_api
)

schema_view_without_ui = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1'
    ),
    public=True,
    patterns=urlpatterns_api
)

urlpatterns = urlpatterns_api + [
    url(r'^$', schema_view.with_ui('swagger',
                                   cache_timeout=0), name='schema-swagger-ui'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view_without_ui.without_ui(cache_timeout=0), name='schema-json')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
