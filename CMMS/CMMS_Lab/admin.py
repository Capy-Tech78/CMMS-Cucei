from django.contrib import admin
from .models import EquipoMedico, PerfilUsuario, ReservaEquipo, FalloReportado, HorarioBiomedico

admin.site.register(EquipoMedico)
admin.site.register(PerfilUsuario)
admin.site.register(ReservaEquipo)
admin.site.register(FalloReportado)
admin.site.register(HorarioBiomedico)
