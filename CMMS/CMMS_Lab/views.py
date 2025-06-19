from django.shortcuts import render
from django.http import HttpResponse
from .models import EquipoMedico, PerfilUsuario


def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'equipos/lista.html', {'equipos': equipos})

