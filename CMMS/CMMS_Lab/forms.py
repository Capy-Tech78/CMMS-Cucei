from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EquipoMedico, PerfilUsuario, FalloReportado, HorarioBiomedico

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
    email = forms.EmailField(required=True, label='Correo electrónico')
    matricula = forms.CharField(required=True, label='Matrícula')
    telefono = forms.CharField(required=False, label='Teléfono')
    especialidad = forms.CharField(required=False, label='Especialidad')
    rol = forms.ChoiceField(choices=PerfilUsuario._meta.get_field('rol').choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if PerfilUsuario.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("Esta matrícula ya está registrada.")
        return matricula

class FalloReportadoForm(forms.ModelForm):
    class Meta:
        model = FalloReportado
        fields = ['equipo', 'descripcion', 'atendido'] 
        labels = {
            'equipo': 'Equipo afectado',
            'descripcion': 'Descripción del fallo',
            'atendido': '¿Atendido?',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

class HorarioBiomedicoForm(forms.ModelForm):
    class Meta:
        model = HorarioBiomedico
        fields = ['biomedico', 'dia_semana', 'hora_inicio', 'hora_fin']
        labels = {
            'biomedico': 'Biomédico',
            'dia_semana': 'Día de la semana',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
        }
        widgets = {
            'dia_semana': forms.Select(),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }