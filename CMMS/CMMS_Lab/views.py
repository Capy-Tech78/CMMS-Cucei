from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import EquipoMedicoForm, FormularioLogin, RegistroBiomedicoForm
from .models import EquipoMedico, PerfilUsuario, FalloReportado, HorarioBiomedico, ReservaEquipo

# Vista pública de inicio
def inicio_publico(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'inicio.html')

# Vista protegida para el dashboard del sistema
@login_required
def dashboard(request):
    perfil = request.user.perfilusuario

    if perfil.rol == 'admin_sistema':
        total_usuarios = PerfilUsuario.objects.count()
        total_equipos = EquipoMedico.objects.count()
        total_fallos = FalloReportado.objects.count()
        total_horarios = HorarioBiomedico.objects.count()
        total_reservas = ReservaEquipo.objects.count()

        return render(request, 'dashboard.html', {
            'total_usuarios': total_usuarios,
            'total_equipos': total_equipos,
            'total_fallos': total_fallos,
            'total_horarios': total_horarios,
            'total_reservas': total_reservas,
        })
    
    return render(request, 'dashboard.html')

# Vista para mostrar los equipos médicos
@login_required
def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

# Vista para registrar un nuevo equipo médico
@login_required
def registrar_equipo(request):
    perfil = request.user.perfilusuario

    if perfil.rol not in ['biomedico', 'admin_sistema']:
        return redirect('lista_equipos')

    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoMedicoForm()

    return render(request, 'equipos/registrar_equipo.html', {'form': form})

# Vista para registrar un usuario biomédico
@login_required
def registrar_biomedico(request):
    if not request.user.perfilusuario.rol == 'admin_sistema':
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroBiomedicoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                rol=form.cleaned_data.get('rol'),
                matricula=form.cleaned_data.get('matricula'),
                telefono=form.cleaned_data.get('telefono'),
                especialidad=form.cleaned_data.get('especialidad')
            )
            return redirect('lista_usuarios')
    else:
        form = RegistroBiomedicoForm()

    return render(request, 'usuarios/registrar_biomedico.html', {'form': form})

# Vista personalizada para el login
def login_view(request):
    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = FormularioLogin()

    return render(request, 'usuarios/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('inicio_publico')

# ---------------------------
# NUEVAS VISTAS AÑADIDAS 
# ---------------------------

# Lista de usuarios
@login_required
def lista_usuarios(request):
    if request.user.perfilusuario.rol != 'admin_sistema':
        return redirect('dashboard')
    usuarios = PerfilUsuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

# Lista de fallos reportados
@login_required
def lista_fallos(request):
    fallos = FalloReportado.objects.all()
    return render(request, 'fallos/lista.html', {'fallos': fallos})

# Lista de horarios biomédicos
@login_required
def lista_horarios(request):
    horarios = HorarioBiomedico.objects.all()
    return render(request, 'horarios/lista.html', {'horarios': horarios})

# Lista de reservas de equipos
@login_required
def lista_reservas(request):
    reservas = ReservaEquipo.objects.all()
    return render(request, 'reservas/lista.html', {'reservas': reservas})

# Vista para crear un fallo reportado
@login_required
def crear_fallo(request):
    # (formulario aún no creado, por ahora solo pantalla de prueba)
    return render(request, 'fallos/crear.html')

# Vista para crear horario
@login_required
def crear_horario(request):
    # (formulario aún no creado, por ahora solo pantalla de prueba)
    return render(request, 'horarios/crear.html')

# Vista para crear reserva
@login_required
def crear_reserva(request):
    # (formulario aún no creado, por ahora solo pantalla de prueba)
    return render(request, 'reservas/crear.html')
