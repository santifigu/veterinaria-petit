from django.shortcuts import render
from .models import Producto, CategoriaProd
from tutor.models import Tutor

def tienda(request, template_name='tienda/tienda.html'):
    todos = Producto.objects.filter(disponibilidad=True).select_related('categoria')
    categorias = CategoriaProd.objects.all()

    # Separar combos del resto
    combos_productos = todos.filter(categoria__nombre__icontains='combo')
    productos = todos.exclude(categoria__nombre__icontains='combo')

    # Búsqueda
    q = request.GET.get('q', '')
    if q:
        productos = productos.filter(nombre__icontains=q) | productos.filter(descripcion__icontains=q)
        combos_productos = combos_productos.filter(nombre__icontains=q) | combos_productos.filter(descripcion__icontains=q)

    # Filtro por categoría
    categoria_id = request.GET.get('categoria', '')
    if categoria_id:
        productos = todos.filter(categoria__id=categoria_id)
        combos_productos = Producto.objects.none()

    # Ordenamiento
    orden = request.GET.get('orden', '')
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')

    context = {
        'productos': productos,
        'combos_productos': combos_productos,
        'categorias': categorias,
        'q': q,
        'categoria_id': categoria_id,
        'orden': orden,
    }
    return render(request, template_name, context)

def checkout(request, template_name='tienda/checkout.html'):
    nombre = ''
    email = ''
    telefono = ''
    
    if request.user.is_authenticated:
        nombre = request.user.get_full_name() or request.user.username
        email = request.user.email
        try:
            tutor = request.user.tutor  # relación inversa directa
            telefono = tutor.telefono
        except Tutor.DoesNotExist:
            pass

    return render(request, template_name, {
        'nombre': nombre,
        'email': email,
        'telefono': telefono,
    })

def confirmado(request, template_name='tienda/confirmado.html'):
    return render(request, template_name)

def no_confirmado(request, template_name='tienda/no_confirmado.html'):
    return render(request, template_name)

def pendiente(request, template_name='tienda/pendiente.html'):
    return render(request, template_name)