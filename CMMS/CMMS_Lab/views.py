from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import EquipoMedico, PerfilUsuario, FalloReportado, HorarioBiomedico, ReservaEquipo
from .forms import EquipoMedicoForm, FormularioLogin, RegistroBiomedicoForm
from .forms import FalloReportadoForm, HorarioBiomedicoForm, ReservaEquipoForm

# Vista pública de inicio
def inicio_publico(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'inicio.html')

# Vista para el dashboard del sistema
@login_required
def dashboard(request):
    perfil = request.user.perfilusuario
    rol = perfil.rol

    context = {
        'rol': rol  # esto se puede usar en el template directamente
    }

    if rol == 'admin_sistema':
        context.update({
            'total_usuarios': PerfilUsuario.objects.count(),
            'total_equipos': EquipoMedico.objects.count(),
            'total_fallos': FalloReportado.objects.count(),
            'total_horarios': HorarioBiomedico.objects.count(),
            'total_reservas': ReservaEquipo.objects.count(),
        })

    return render(request, 'dashboard.html', context) # Retorna siempre el mismo template y un solo diccionario 'context'

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

# Lista de usuarios
@login_required
def lista_usuarios(request):
    if request.user.perfilusuario.rol != 'admin_sistema':
        return redirect('dashboard')
    usuarios = PerfilUsuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

# Lista de usuarios pero solo con nombre y matricula, solo para biomedicos 
@login_required
def ver_usuarios_biomedico(request):
    if request.user.perfilusuario.rol != 'biomedico':
        return redirect('dashboard')

    perfiles = PerfilUsuario.objects.select_related('user')
    return render(request, 'usuarios/ver_limitado.html', {'perfiles': perfiles})

# Lista de equipos médicos
@login_required
def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

# Lista de fallos reportados
@login_required
def lista_fallos(request):
    fallos = FalloReportado.objects.all().order_by('-fecha_reporte')  # Orden de más recientes primero
    return render(request, 'fallos/lista.html', {'fallos': fallos})

# Lista de horarios biomédicos
@login_required
def lista_horarios(request):
    horarios = HorarioBiomedico.objects.select_related('biomedico').order_by('dia_semana', 'hora_inicio')
    return render(request, 'horarios/lista.html', {'horarios': horarios})

# Lista de reservas de equipos
@login_required
def lista_reservas(request):
    reservas = ReservaEquipo.objects.select_related('equipo', 'usuario').order_by('-fecha_reserva', '-hora_inicio')
    return render(request, 'reservas/lista.html', {'reservas': reservas})

# Registrar un usuario
@login_required
def registrar_biomedico(request):
    # Permitir acceso a admin y biomedico
    if request.user.perfilusuario.rol not in ['admin_sistema', 'biomedico']:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroBiomedicoForm(request.POST)

        # Antes de validar, Se limitan las opciones si no es admin
        if request.user.perfilusuario.rol != 'admin_sistema':
            form.fields['rol'].choices = [
                ('estudiante', 'Estudiante'),
                ('biomedico', 'Biomedico'),
            ]

        if form.is_valid():
            # Validación extra por seguridad: evitar que un biomédico cree un admin
            rol_seleccionado = form.cleaned_data.get('rol')
            if request.user.perfilusuario.rol != 'admin_sistema' and rol_seleccionado == 'admin_sistema':
                form.add_error('rol', 'No tienes permisos para asignar rol de administrador.')
            else:
                user = form.save(commit=False)
                user.save()
                PerfilUsuario.objects.create(
                    user=user,
                    rol=rol_seleccionado,
                    matricula=form.cleaned_data.get('matricula'),
                    telefono=form.cleaned_data.get('telefono'),
                    especialidad=form.cleaned_data.get('especialidad')
                )
                return redirect('lista_usuarios')
    else:
        form = RegistroBiomedicoForm()
        if request.user.perfilusuario.rol != 'admin_sistema':
            # Limitar opciones si no es admin
            form.fields['rol'].choices = [
                ('estudiante', 'Estudiante'),
                ('biomedico', 'Biomedico'),
            ]

    return render(request, 'usuarios/registrar_biomedico.html', {'form': form})

# Registrar un nuevo equipo médico
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

# Crear un fallo reportado
@login_required
def crear_fallo(request):
    if request.method == 'POST':
        form = FalloReportadoForm(request.POST)
        if form.is_valid():
            fallo = form.save(commit=False)
            fallo.reportado_por = request.user  # Asigna el usuario que reporta
            fallo.save()
            return redirect('lista_fallos')  # URL
    else:
        form = FalloReportadoForm()
    
    return render(request, 'fallos/crear.html', {'form': form})

# Crear horario
@login_required
def crear_horario(request):
    perfil = request.user.perfilusuario

    # Solo admin o biomedico pueden acceder
    if perfil.rol not in ['admin_sistema', 'biomedico']:
        return redirect('dashboard')

    if request.method == 'POST':
        form = HorarioBiomedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_horarios')
    else:
        form = HorarioBiomedicoForm()

    return render(request, 'horarios/crear.html', {'form': form})

# Crear reserva
@login_required
def crear_reserva(request):
    # Si quieres restringir a admin y biomédico:
    if request.user.perfilusuario.rol not in ['admin_sistema', 'biomedico']:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReservaEquipoForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('lista_reservas')
    else:
        form = ReservaEquipoForm()
    return render(request, 'reservas/crear.html', {'form': form})

# Editar usuario
@login_required
def editar_usuario(request, user_id):
    # Solo admin puede editar usuarios
    if request.user.perfilusuario.rol != 'admin_sistema':
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)
    perfil = get_object_or_404(PerfilUsuario, user=user)

    if request.method == 'POST':
        # Usa el mismo formulario que para registrar, pero con instance
        form = RegistroBiomedicoForm(request.POST, instance=user)
        if form.is_valid():
            # Guarda cambios en User
            user = form.save()

            # Guarda cambios en PerfilUsuario si tienes campos extra
            perfil.matricula = form.cleaned_data.get('matricula')
            perfil.telefono = form.cleaned_data.get('telefono')
            perfil.especialidad = form.cleaned_data.get('especialidad')

            # Validar que solo admin pueda poner rol admin
            nuevo_rol = form.cleaned_data.get('rol')
            if request.user.perfilusuario.rol == 'admin_sistema':
                perfil.rol = nuevo_rol

            perfil.save()

            return redirect('lista_usuarios')
    else:
        # Prellenar formulario con los datos existentes
        form = RegistroBiomedicoForm(instance=user, initial={
            'matricula': perfil.matricula,
            'telefono': perfil.telefono,
            'especialidad': perfil.especialidad,
            'rol': perfil.rol
        })

    return render(request, 'usuarios/editar.html', {'form': form})

# Editar equipo
@login_required
def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(EquipoMedico, id=equipo_id)
    form = EquipoMedicoForm(request.POST or None, request.FILES or None, instance=equipo)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('lista_equipos') 
    return render(request, 'equipos/editar.html', {'form': form, 'equipo': equipo})

# Editar fallo
@login_required
def editar_fallo(request, fallo_id):
    fallo = get_object_or_404(FalloReportado, id=fallo_id)

    if request.user.perfilusuario.rol != 'admin_sistema':
        return redirect('lista_fallos')  # o mostrar error

    if request.method == 'POST':
        form = FalloReportadoForm(request.POST, instance=fallo)
        if form.is_valid():
            form.save()
            return redirect('lista_fallos')
    else:
        form = FalloReportadoForm(instance=fallo)

    return render(request, 'fallos/editar.html', {'form': form, 'fallo': fallo})

# Editar horario
@login_required
def editar_horario(request, horario_id):
    # Verificar rol
    if request.user.perfilusuario.rol not in ['admin_sistema', 'biomedico']:
        return redirect('dashboard')

    # Obtener el horario o dar 404 si no existe
    horario = get_object_or_404(HorarioBiomedico, id=horario_id)

    # Crear formulario con datos existentes
    form = HorarioBiomedicoForm(request.POST or None, instance=horario)

    # Procesar envío de formulario
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('lista_horarios')

    # Renderizar template
    return render(request, 'horarios/editar.html', {'form': form})

# Editar reserva
@login_required
def editar_reserva(request, reserva_id):
    if request.user.perfilusuario.rol not in ['admin_sistema', 'biomedico']:
        return redirect('dashboard')

    reserva = get_object_or_404(ReservaEquipo, id=reserva_id)
    form = ReservaEquipoForm(request.POST or None, instance=reserva)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    return render(request, 'reservas/editar.html', {'form': form})
