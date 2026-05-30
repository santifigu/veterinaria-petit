from django.urls import path
from . import views # Llamamos las vistas desde views

urlpatterns = [
    path('', views.procesar_pedido, name="procesar_pedido"),
]