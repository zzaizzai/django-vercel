# example/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('', Home.as_view(), name='mainhome'),
    path('index', Index.as_view(), name='index_project'),
    path('list',  ProjectList.as_view(), name='project_list'),
    path('detail',  ProjectDetail.as_view(), name='project_detail'),
    path('create_table', create_table, name='create_table_project'),
    path('create', ProjectAdd.as_view(), name='project_create'),
    path('tasks/add', TaskAdd.as_view(), name='task_add'),
    path('tasks/complete', TaskComplete.as_view(), name='task_complete'),
    path('tasks/delete', TaskDelete.as_view(), name='task_delete')
]
