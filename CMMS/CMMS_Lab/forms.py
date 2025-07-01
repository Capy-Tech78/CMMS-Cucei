from django import forms
from .models import EquipoMedico
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

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

class RegistroBiomedicoForm(UserCreationForm):
    email = forms.EmailField(required=True)
    matricula = forms.CharField(required=False)
    telefono = forms.CharField(required=False)
    especialidad = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

def clean_matricula(self):
    matricula = self.cleaned_data['matricula']
    if PerfilUsuario.objects.filter(matricula=matricula).exists():
        raise forms.ValidationError("Esta matrícula ya está registrada.")
    return matricula
