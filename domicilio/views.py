from django.shortcuts import render

# Create your views here.

def domicilio(request, template_name="domicilio/domicilio.html"):
    return render(request, template_name)