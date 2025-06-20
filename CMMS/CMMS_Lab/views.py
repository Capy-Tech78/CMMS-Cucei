from django.shortcuts import render, redirect
from .forms import EquipoMedicoForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import EquipoMedico, PerfilUsuario


def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})


@login_required
def registrar_equipo(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        return redirect('lista_equipos')

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