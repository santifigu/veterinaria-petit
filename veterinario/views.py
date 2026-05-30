from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from .models import Veterinario
from mascota.models import Mascota, RegistroVacunacion, HistorialMedico, Archivo
from turnos.models import Turno

@login_required
def dashboard(request):
    """Dashboard principal del veterinario"""
    try:
        veterinario = request.user.veterinario
    except Veterinario.DoesNotExist:
        messages.error(request, 'No tienes permisos de veterinario')
        return redirect('core:index')
    
    # Obtener estadísticas
    hoy = date.today()
    turnos_hoy = Turno.objects.filter(
        veterinario=veterinario,
        fecha=hoy,
        estado__in=['confirmado', 'en_curso']
    ).select_related('mascota', 'servicio').order_by('hora')
    
    turnos_pendientes = Turno.objects.filter(
        veterinario=veterinario,
        fecha__gte=hoy,
        estado='confirmado'
    ).count()
    
    # Próximos turnos (próximos 7 días)
    proximos_turnos = Turno.objects.filter(
        veterinario=veterinario,
        fecha__range=[hoy, hoy + timedelta(days=7)],
        estado='confirmado'
    ).select_related('mascota', 'servicio').order_by('fecha', 'hora')[:10]
    
    # Mascotas atendidas recientemente
    mascotas_recientes = Mascota.objects.filter(
        turnos__veterinario=veterinario,
        turnos__estado='completado'
    ).distinct().order_by('-turnos__fecha')[:5]
    
    context = {
        'veterinario': veterinario,
        'turnos_hoy': turnos_hoy,
        'turnos_pendientes': turnos_pendientes,
        'proximos_turnos': proximos_turnos,
        'mascotas_recientes': mascotas_recientes,
    }
    
    return render(request, 'veterinario/dashboard.html', context)

@login_required
def detalle_paciente(request, mascota_id):
    """Vista detallada de un paciente/mascota"""
    try:
        veterinario = request.user.veterinario
    except Veterinario.DoesNotExist:
        messages.error(request, 'No tienes permisos de veterinario')
        return redirect('core:index')
    
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Obtener todo el historial
    historial = HistorialMedico.objects.filter(mascota=mascota).order_by('-fecha')
    vacunas = RegistroVacunacion.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')
    turnos = Turno.objects.filter(mascota=mascota).order_by('-fecha', '-hora')
    archivos = Archivo.objects.filter(mascota=mascota).order_by('-fecha')
    
    context = {
        'veterinario': veterinario,
        'mascota': mascota,
        'historial': historial,
        'vacunas': vacunas,
        'turnos': turnos,
        'archivos': archivos,
    }
    
    return render(request, 'veterinario/detalle_paciente.html', context)

@login_required
def agregar_historial(request, mascota_id):
    """Agregar registro al historial médico"""
    try:
        veterinario = request.user.veterinario
    except Veterinario.DoesNotExist:
        messages.error(request, 'No tienes permisos de veterinario')
        return redirect('core:index')
    
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    if request.method == 'POST':
        HistorialMedico.objects.create(
            mascota=mascota,
            veterinario=veterinario,
            tipo=request.POST.get('tipo'),
            fecha=request.POST.get('fecha'),
            motivo_consulta=request.POST.get('motivo_consulta'),
            diagnostico=request.POST.get('diagnostico'),
            tratamiento=request.POST.get('tratamiento'),
            medicamentos=request.POST.get('medicamentos', ''),
            examenes=request.POST.get('examenes', ''),
            peso=request.POST.get('peso') or None,
            temperatura=request.POST.get('temperatura') or None,
            observaciones=request.POST.get('observaciones', ''),
            proxima_visita=request.POST.get('proxima_visita') or None
        )
        
        messages.success(request, 'Historial médico registrado correctamente')
        return redirect('veterinario:detalle_paciente', mascota_id=mascota_id)
    
    return render(request, 'veterinario/agregar_historial.html', {'mascota': mascota})