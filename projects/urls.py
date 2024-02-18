# example/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('', index),
    path('index', Index.as_view(), name='index_project'),
]