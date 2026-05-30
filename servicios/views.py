from django.shortcuts import render

# Create your views here.

def servicios(request, template_name='servicios/servicios.html'):
    return render(request, template_name)