# example/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('', index),
    path('index', Index.as_view(), name='index_project'),
    path('list',  ProjectList.as_view(), name='project_list'),
    path('create_table', create_table, name='create_table_project'),
]