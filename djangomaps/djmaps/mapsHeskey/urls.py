from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^request/', views.request_page, name='request'),
    re_path('', views.default_map, name='default'),
]
