"""camper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from camper.core.viewsets import StatsView
from camper.values.viewsets import ValueViewSet
from camper.events.viewsets import EventViewSet
from camper.devices.viewsets import DeviceViewSet
from camper.controls.viewsets import (
    ControlViewSet,
    SwitchControlViewSet,
    RangeControlViewSet
)
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter

schema_view = get_swagger_view(title='Camper API')

router = DefaultRouter()

router.register('values', ValueViewSet, base_name='value')
router.register('events', EventViewSet, base_name='event')
router.register('devices', DeviceViewSet, base_name='device')
router.register('channels', DeviceViewSet, base_name='channel')
router.register('stats', StatsView, base_name='stats')
router.register('controls/switches', SwitchControlViewSet, base_name='switchcontrol')
router.register('controls/ranges', RangeControlViewSet, base_name='rangecontrol')
router.register('controls', ControlViewSet, base_name='control')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^api/', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, dict(
        document_root=settings.MEDIA_ROOT,
    ), name='media'),
    url(r'^$', schema_view),
]

