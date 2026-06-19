from django.shortcuts import render
from carro.carro import Carro

def index(request, template_name='core/index.html'):
    carro = Carro(request) # Aseguramos que el carro esté disponible en la vista
    return render(request, template_name)

def nosotros(request, template_name='core/nosotros.html'):
    return render(request, template_name)

# Vistas para políticas y términos
def politica(request, template_name='core/politica.html'):
    return render(request, template_name)

def terminos(request, template_name='core/terminos.html'):
    return render(request, template_name)

def cookies(request, template_name='core/cookies.html'):
    return render(request, template_name)

# Errores personalizados
def error_404(request, exception=None):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def error_403(request, exception=None):
    return render(request, '403.html', status=403)