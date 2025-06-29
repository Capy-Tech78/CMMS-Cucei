from django import forms
from .models import EquipoMedico
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class FormularioLogin(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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
        labels = {
            'nombre': 'Nombre del equipo',
            'modelo': 'Modelo',
            'fabricante': 'Fabricante',
            'numero_serie': 'Número de serie',
            'ubicacion': 'Ubicación',
            'estado': 'Estado',
            'fecha_adquisicion': 'Fecha de adquisición',
            'mantenimiento_preventivo': 'Próximo mantenimiento preventivo',
            'imagen': 'Imagen del equipo',
        }