from django.contrib import admin  
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Página pública de bienvenida
    path('', views.inicio_publico, name='inicio_publico'),

    # Dashboard después de iniciar sesión
    path('dashboard/', views.dashboard, name='dashboard'),

    # Autenticación y gestión de usuarios
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrar-biomedico/', views.registrar_biomedico, name='registrar_biomedico'),

    # Usuarios (solo admin_sistema)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),

    # Equipos Médicos
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/registrar/', views.registrar_equipo, name='registrar_equipo'),
    path('equipos/editar/<int:equipo_id>/', views.editar_equipo, name='editar_equipo'),

    # Fallos Reportados
    path('fallos/', views.lista_fallos, name='lista_fallos'),
    path('fallos/editar/<int:fallo_id>/', views.editar_fallo, name='editar_fallo'),

    # Horarios de Biomédicos
    path('horarios/', views.lista_horarios, name='lista_horarios'),
    path('horarios/editar/<int:horario_id>/', views.editar_horario, name='editar_horario'),

    # Reservas de Equipo
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/editar/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),

        # Rutas faltantes para vista del dashboard
    path('usuarios/ver/', views.lista_usuarios, name='ver_usuarios'),

    path('fallos/ver/', views.lista_fallos, name='ver_fallos'),
    path('horarios/ver/', views.lista_horarios, name='ver_horarios'),
    path('reservas/ver/', views.lista_reservas, name='ver_reservas'),

    # Otras rutas para creación
    path('fallos/crear/', views.crear_fallo, name='crear_fallo'),
    path('horarios/crear/', views.crear_horario, name='crear_horario'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)