from django import forms
from .models import Turno, Servicio
from datetime import datetime, time, timedelta

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'fecha', 'hora', 'nombre_mascota', 'email_cliente', 'telefono_cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'hidden'}),
            'hora': forms.TimeInput(attrs={'type': 'hidden'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < datetime.now().date():
            raise forms.ValidationError("No puedes reservar un turno en una fecha pasada.")
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        # Verificar que el turno no esté ocupado
        if fecha and hora:
            if Turno.objects.filter(fecha=fecha, hora=hora, estado__in=['pendiente', 'confirmado']).exists():
                raise forms.ValidationError("Este horario ya está reservado. Por favor, elige otro.")
        
        return cleaned_data