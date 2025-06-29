from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import EquipoMedicoForm
from django.http import HttpResponse
from .models import EquipoMedico, PerfilUsuario
from .forms import FormularioLogin, EquipoMedicoForm
from django.contrib.auth import logout

# Vista para mostrar los equipos médicos
@login_required
def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

# Vista para mostrar biomédicos
def lista_biomedicos(request):
    biomedicos = PerfilUsuario.objects.filter(rol='biomedico')
    return render(request, 'biomedicos.html', {'biomedicos': biomedicos})

def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

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

def logout_view(request):
    logout(request)
    return redirect('login')
