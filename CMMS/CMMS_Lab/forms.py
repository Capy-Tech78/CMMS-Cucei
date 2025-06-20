from django import forms
from .models import EquipoMedico

class EquipoMedicoForm(forms.ModelForm):
    class Meta:
        model = EquipoMedico
        fields = [
            'nombre',
            'modelo',
            'fabricante',
            'numero_serie',
            'ubicacion',
            'estado',
            'fecha_adquisicion',
            'mantenimiento_preventivo',
            'imagen'
        ]
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
            'mantenimiento_preventivo': forms.DateInput(attrs={'type': 'date'}),
        }