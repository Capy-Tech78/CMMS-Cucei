from django.db import models
from django.contrib.auth.models import User

# ----------------------------
# Modelo de Equipos Médicos
# ----------------------------
class EquipoMedico(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True)
    fabricante = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('en_mantenimiento', 'En mantenimiento'),
        ('fuera_de_servicio', 'Fuera de servicio'),
    ])
    fecha_adquisicion = models.DateField(null=True, blank=True)
    mantenimiento_preventivo = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='equipos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"


# ------------------------------------------
# Perfil extendido para distinguir roles
# ------------------------------------------
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ('estudiante', 'Estudiante'),
        ('biomedico', 'Biomedico'),
        ('admin_sistema', 'Administrador del sistema'),
    ])
    matricula = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


# -------------------------------
# Modelo para Reservas de Equipo
# -------------------------------
class ReservaEquipo(models.Model):
    equipo = models.ForeignKey(EquipoMedico, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.equipo} reservado por {self.usuario.username}"


# --------------------------------
# Modelo para Fallos Reportados
# --------------------------------
class FalloReportado(models.Model):
    equipo = models.ForeignKey(EquipoMedico, on_delete=models.CASCADE)
    reportado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    atendido = models.BooleanField(default=False)
    fecha_solucion = models.DateTimeField(null=True, blank=True)
    solucionado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fallos_solucionados')

    def __str__(self):
        return f"Fallo en {self.equipo} - {'Atendido' if self.atendido else 'Pendiente'}"


# -----------------------------
# Horarios de Biomédicos
# -----------------------------
class HorarioBiomedico(models.Model):
    biomedico = models.ForeignKey(User, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=[
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.biomedico.username} - {self.dia_semana} {self.hora_inicio} a {self.hora_fin}"
