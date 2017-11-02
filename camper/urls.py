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
from django.contrib import admin
from camper.core.viewsets import StatsView
from camper.channels.viewsets import InputChannelViewSet
from camper.values.viewsets import ValueViewSet
from camper.events.viewsets import EventViewSet
from camper.things.viewsets import ThingViewSet
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter

schema_view = get_swagger_view(title='Camper API')

router = DefaultRouter()

router.register('channels', InputChannelViewSet, base_name='inputchannel')
router.register('values', ValueViewSet, base_name='value')
router.register('events', EventViewSet, base_name='event')
router.register('things', ThingViewSet, base_name='thing')
router.register('stats', StatsView, base_name='stats')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^api/', include(router.urls)),
    url(r'^$', schema_view),
]

