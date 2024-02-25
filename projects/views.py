# example/views.py
from datetime import datetime
from typing import Any
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.db import connection
from core.common_funcs import dictfetchall
from django.http import HttpResponse
from .models import Projects, DemoData

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
        
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM projects where id = {project_id}")
            projects = dictfetchall(cursor)
        
        # No project return list page
        if projects is None or len(projects) == 0:
            return redirect('/projects/list')
        
        context['project'] = projects[0]
        
        
        return render(request, self.template_name, context)


class ProjectList(TemplateView):
    template_name = 'project/project_list.html'
    
    def get(self, request):
        context = self.get_context_data()
        projects = Projects.get_all()
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
            Projects(title = title,description = description, created_user_name= "User1 for Demo", created_user_id = created_user_id).create_a_project()
        except Exception as e:
            print(e)
            
        
        return redirect('/projects/list')
    
def create_table(request):
    try:
        Projects.create_table()  
        DemoData().create_demo_data_projects()
    except Exception as e:
        print(e)
        return HttpResponse(e)
    return HttpResponse('good')