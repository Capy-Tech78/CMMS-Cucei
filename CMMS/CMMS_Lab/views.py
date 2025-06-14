from django.shortcuts import render
from django.http import HttpResponse
from .models import EquipoMedico, PerfilUsuario

# Vista para mostrar los equipos médicos
def lista_equipos(request):
    equipos = EquipoMedico.objects.all()
    texto = "<h1>Equipos Médicos</h1><ul>"
    for e in equipos:
        texto += f"<li>{e.nombre} - {e.estado}</li>"
    texto += "</ul>"
    return HttpResponse(texto)

# Vista para mostrar biomédicos
def lista_biomedicos(request):
    biomedicos = PerfilUsuario.objects.filter(rol='biomedico')
    return render(request, 'biomedicos.html', {'biomedicos': biomedicos})


def hola(request):
    return HttpResponse("Chingas a tu madre cabron")

