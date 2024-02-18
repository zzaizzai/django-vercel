# example/views.py
from datetime import datetime
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect

from django.http import HttpResponse

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
    template_name = 'project_index.html'
    
    def get(self, reqeust):
        context = self.get_context_data()
        
        return render(reqeust, self.template_name, context)