from django.urls import path
from . import views # Llamamos las vistas desde views

urlpatterns = [
    path('', views.index, name="index"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('politica', views.politica, name="politica"),
    path('terminos', views.terminos, name="terminos"),
    path('cookies', views.cookies, name="cookies"),
    
]