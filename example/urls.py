# example/urls.py
from django.urls import path

from example.views import Home


urlpatterns = [
    path('', Home.as_view(), name='mainhome'),
]