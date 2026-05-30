from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import date
from tutor.models import Tutor

def perfil_tutor(request):
    """Perfil del tutor - Acceso con email"""
    email = request.GET.get('email')
    
    if not email:
        return render(request, 'tutor/perfil_tutor_login.html')
    
    try:
        tutor = Tutor.objects.get(email=email)
        
        # Importamos aquí para evitar imports circulares
        from .models import Mascota
        from .models import Turno
        
        mascotas = Mascota.objects.filter(tutor=tutor, activo=True)
        
        # Próximos turnos
        hoy = date.today()
        proximos_turnos = Turno.objects.filter(
            Q(email_cliente=email) | Q(mascota__tutor=tutor),
            fecha__gte=hoy,
            estado__in=['pendiente', 'confirmado']
        ).select_related('servicio', 'mascota').order_by('fecha', 'hora')[:5]
        
        context = {
            'tutor': tutor,
            'mascotas': mascotas,
            'proximos_turnos': proximos_turnos,
        }
        
        return render(request, 'tutor/perfil_tutor.html', context)
        
    except Tutor.DoesNotExist:
        # Si no existe, mostrar formulario de registro
        return render(request, 'tutor/perfil_tutor_registro.html', {'email': email})

def registro_tutor(request):
    """Crear un nuevo tutor"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        # Verificar que no exista el email
        if Tutor.objects.filter(email=email).exists():
            messages.error(request, 'Este email ya está registrado')
            return redirect('tutor:perfil')
        
        # Crear tutor
        Tutor.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        
        messages.success(request, '¡Registro exitoso!')
        return redirect(f'/tutor/perfil/?email={email}')
    
    return render(request, 'tutor/registro_tutor.html')

def actualizar_tutor(request, tutor_id):
    """Actualizar datos del tutor"""
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    if request.method == 'POST':
        tutor.nombre = request.POST.get('nombre')
        tutor.apellido = request.POST.get('apellido')
        tutor.telefono = request.POST.get('telefono')
        tutor.direccion = request.POST.get('direccion')
        tutor.save()
        
        messages.success(request, 'Datos actualizados correctamente')
        return redirect(f'/tutor/perfil/?email={tutor.email}')
    
    return render(request, 'tutor/editar_tutor.html', {'tutor': tutor})