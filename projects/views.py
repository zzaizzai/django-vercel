# example/views.py
from datetime import datetime
from typing import Any
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.db import connection
from core.common_funcs import dictfetchall
from django.http import HttpResponse
from .models import Projects


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
    

def create_table(request):
    a= Projects
    a.create_table() 
    a.create_demo_data()
    return HttpResponse('good')