from django.views.generic.base import TemplateView
from django.shortcuts import render

class Home(TemplateView):
    template_name = 'core/home.html'
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    