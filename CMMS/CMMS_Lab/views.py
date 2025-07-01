from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EquipoMedicoForm, FormularioLogin, RegistroBiomedicoForm
from .models import EquipoMedico, PerfilUsuario

# Vista para mostrar los equipos médicos
@login_required
def registrar_biomedico(request):
    if not request.user.perfilusuario.rol == 'biomedico':
        return redirect('lista_equipos')  # protección

    if request.method == 'POST':
        form = RegistroBiomedicoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                rol='biomedico',
                matricula=form.cleaned_data.get('matricula'),
                telefono=form.cleaned_data.get('telefono'),
                especialidad=form.cleaned_data.get('especialidad')
            )
            return redirect('lista_equipos')  # o alguna confirmación
    else:
        form = RegistroBiomedicoForm()

    return render(request, 'usuarios/registrar_biomedico.html', {'form': form})

def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

# Vista para mostrar biomédicos
def lista_biomedicos(request):
    biomedicos = PerfilUsuario.objects.filter(rol='biomedico')
    return render(request, 'biomedicos.html', {'biomedicos': biomedicos})

# Vista para registrar un nuevo equipo médico
@login_required
def registrar_equipo(request):
    perfil = request.user.perfilusuario

    if perfil.rol != 'biomedico':
        return redirect('lista_equipos')

    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoMedicoForm()

    return render(request, 'equipos/registrar_equipo.html', {'form': form})

# Vista personalizada para el login con formulario en español
def login_view(request):
    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('lista_equipos')
    else:
        form = FormularioLogin()

    return render(request, 'usuarios/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')
