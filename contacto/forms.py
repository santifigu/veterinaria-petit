from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'apellido', 'email', 'telefono', 'nombre_mascota', 'tipo_consulta', 'mensaje']
        widgets = {
            'tipo_consulta': forms.Select(
                attrs={
                    'class': 'w-full px-5 py-4 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800 focus:ring-2 focus:ring-primary outline-none transition-all appearance-none'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega opción vacía al inicio del select
        self.fields['tipo_consulta'].empty_label = 'Seleccionar tipo de consulta'