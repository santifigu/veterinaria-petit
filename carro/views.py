from django.shortcuts import redirect
from .carro import Carro
from tienda.models import Producto # Asegúrate de importar tu modelo

def agregar_producto(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    # Esto te devuelve a la misma página donde estabas (Tienda o Checkout)
    return redirect(request.META.get('HTTP_REFERER', 'tienda'))

def restar_producto(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.restar(producto=producto)
    return redirect(request.META.get('HTTP_REFERER', 'tienda'))

def eliminar_producto(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect(request.META.get('HTTP_REFERER', 'tienda'))

def limpiar_carro(request):
    carro = Carro(request) # Creamos una instancia de la clase Carro para poder acceder a sus métodos
    carro.limpiar_carro() # Limpiamos el carro utilizando el método limpiar_carro de la clase Carro
    return redirect("tienda") # Redirigimos a la página de la tienda para mostrar el carro actualizado

