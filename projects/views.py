# example/views.py
from datetime import datetime
from django.urls import reverse
from typing import Any
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.db import connection
from core.common_funcs import dictfetchall
from django.http import HttpResponse, JsonResponse
from .models import Project, DemoData, Task
from datetime import date
from django.utils import timezone

class Home(TemplateView):
    template_name = 'core/home.html'
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
class Index(TemplateView):
    template_name = 'project/project_index.html'
    
    def get(self, request):
        context = self.get_context_data()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM test")
            row = dictfetchall(cursor)

        context['test'] = row
        return render(request, self.template_name, context)
    

class ProjectDetail(TemplateView):
    template_name = 'project/project_detail.html'
    
    
    def get(self, request):
        
        context = self.get_context_data()
        project_id = request.GET.get('id')

        # No id params, return list page
        if project_id is None:
            return redirect('/projects/list')
        
        project = Project.get_one_project(project_id=project_id)
        
        # No project return list page
        if project is None:
            return redirect('/projects/list')
        
        context['project'] = project
        context['tasks'] = project.get_all_tasks()
        context['today'] = date.today()
        
        return render(request, self.template_name, context)
    
class TaskAdd(TemplateView):
    
    def post(self, request):
        print(request.POST)
        parent_project_id = request.POST.get('parent_project_id')
        plan_date = request.POST.get('plan_date')
        title = request.POST.get('title')
        created_user_id = 1 # for temp

        plan_datetime =  datetime.strptime(plan_date, '%Y-%m-%d')
        plan_datetime_with_tz = timezone.make_aware(plan_datetime, timezone=timezone.get_current_timezone())


        if len(title) < 3 :
            return redirect(f'/projects/detail?id={parent_project_id}')
        
        try:
            Task(title =title, description = '', created_user_name= "User1 for Demo", created_user_id = created_user_id, parent_project_id=parent_project_id, plan_date=plan_datetime_with_tz).create_a_task()
        except Exception as e:
            print(e)
        
        if parent_project_id:
            return redirect(f'/projects/detail?id={parent_project_id}')
        else:
            return redirect('/projects/list')

    
class TaskDelete(TemplateView):
    
    def post(self, request):
        task_id = request.POST.get('id')
        print(request)
        
        if task_id is None:
            response_data = {'success': False, 'message': 'There is no task id'}
            return JsonResponse(response_data)
        
        try:
            Task.delete_with_id(task_id=task_id)
            response_data = {'success': True, 'message': 'Task deleted successfully.'}
            return JsonResponse(response_data)
        
        except Exception as e:
            # 실패시 예외 처리
            print(e)
            response_data = {'success': False, 'message': str(e)}
            return JsonResponse(response_data, status=400) 


class ProjectList(TemplateView):
    template_name = 'project/project_list.html'
    
    def get(self, request):
        context = self.get_context_data()
        projects = Project.get_all()
        context['projects'] = projects
        
        return render(request, self.template_name, context)
    
    
class ProjectAdd(TemplateView):
    template_name = 'project/project_create.html'
    
    
    def get(self, request):
        
        context = self.get_context_data()
        
        return render(request, self.template_name, context)

    def post(self, request):

        description = 'description for demo'
        
        try:
            title = str(request.POST.get('title'))
            created_user_id = int(request.POST.get('created_user_id'))
        except ValueError:
            return redirect('/projects/list')
        
        try:
            Project(title = title,description = description, created_user_name= "User1 for Demo", created_user_id = created_user_id).create_a_project()
        except Exception as e:
            print(e)
            
        
        return redirect('/projects/list')
    
def create_table(request):
    try:
        Project.create_table()  
        Task.create_table()
        DemoData().create_demo_data_projects()
    except Exception as e:
        print(e)
        return HttpResponse(e)
    return HttpResponse('good')