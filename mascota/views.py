from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mascota, RegistroVacunacion, HistorialMedico, Archivo
from tutor.models import Tutor

def cartilla_sanitaria(request, mascota_id):
    """Cartilla sanitaria digital"""
    mascota = get_object_or_404(Mascota, id=mascota_id)
    vacunas = RegistroVacunacion.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')
    
    context = {
        'mascota': mascota,
        'vacunas': vacunas,
    }
    
    return render(request, 'mascota/cartilla_sanitaria.html', context)

def agregar_mascota(request):
    """Agregar una nueva mascota"""
    if request.method == 'POST':
        # Obtener el tutor por email
        email_tutor = request.POST.get('email_tutor')
        tutor = get_object_or_404(Tutor, email=email_tutor)
        
        # Manejar la foto si se subió
        foto = request.FILES.get('foto')
        
        # Crear la mascota
        Mascota.objects.create(
            tutor=tutor,
            nombre=request.POST.get('nombre'),
            tipo=request.POST.get('tipo'),
            raza=request.POST.get('raza'),
            sexo=request.POST.get('sexo'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
            color=request.POST.get('color'),
            peso=request.POST.get('peso') or None,
            microchip=request.POST.get('microchip', ''),
            observaciones=request.POST.get('observaciones', ''),
            foto=foto
        )
        
        messages.success(request, '¡Mascota agregada exitosamente!')
        return redirect(f'/tutor/perfil/?email={email_tutor}')
    
    return render(request, 'mascota/agregar_mascota.html')

def editar_mascota(request, mascota_id):
    """Editar datos de una mascota"""
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    if request.method == 'POST':
        mascota.nombre = request.POST.get('nombre')
        mascota.tipo = request.POST.get('tipo')
        mascota.raza = request.POST.get('raza')
        mascota.sexo = request.POST.get('sexo')
        mascota.color = request.POST.get('color')
        mascota.peso = request.POST.get('peso') or None
        mascota.microchip = request.POST.get('microchip', '')
        mascota.observaciones = request.POST.get('observaciones', '')
        mascota.save()
        
        messages.success(request, 'Mascota actualizada correctamente')
        return redirect(f'/tutor/perfil/?email={mascota.tutor.email}')
    
    return render(request, 'mascota/editar_mascota.html', {'mascota': mascota})

def eliminar_mascota(request, mascota_id):
    """Desactivar una mascota"""
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.activo = False
    mascota.save()
    
    messages.success(request, 'Mascota desactivada correctamente')
    return redirect(f'/tutor/perfil/?email={mascota.tutor.email}')

def agregar_vacuna(request, mascota_id):
    """Agregar registro de vacunación"""
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    if request.method == 'POST':
        RegistroVacunacion.objects.create(
            mascota=mascota,
            nombre_vacuna=request.POST.get('nombre_vacuna'),
            fecha_aplicacion=request.POST.get('fecha_aplicacion'),
            proxima_dosis=request.POST.get('proxima_dosis') or None,
            lote=request.POST.get('lote', ''),
            laboratorio=request.POST.get('laboratorio', ''),
            observaciones=request.POST.get('observaciones', '')
        )
        
        messages.success(request, 'Vacuna registrada correctamente')
        return redirect('mascota:cartilla_sanitaria', mascota_id=mascota_id)
    
    return render(request, 'mascota/agregar_vacuna.html', {'mascota': mascota})