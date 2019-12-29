from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from kyykka import views

urlpatterns = [
    path('', views.signup),
    path('success', views.success, name='complete'),
]
