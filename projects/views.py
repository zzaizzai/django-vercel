# example/views.py
from datetime import datetime
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.db import connection
from core.common_funcs import dictfetchall
from django.http import HttpResponse
from .models import Project


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>projects page Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

class Index(TemplateView):
    template_name = 'project/project_index.html'
    
    def get(self, reqeust):
        context = self.get_context_data()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM test")
            row = dictfetchall(cursor)

        context['test'] = row
        return render(reqeust, self.template_name, context)
    

class ProjectList(TemplateView):
    template_name = 'project/project_list.html'
    
    def get(self, reqeust):
        context = self.get_context_data()
        projects = Project.get_all()
        context['projects'] = projects
        
        return render(reqeust, self.template_name, context)
    

def create_table(request):
    a= Project
    a.create_table() 
    a.create_demo_data()
    return HttpResponse('good')