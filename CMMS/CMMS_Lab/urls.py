from django.contrib import admin 
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Registrar biomedicos
    path('registrar-biomedico/', views.registrar_biomedico, name='registrar_biomedico'),
    # Lista de equipos
    path('', views.lista_equipos, name='lista_equipos'),
    path('registrar/', views.registrar_equipo, name='registrar_equipo'),
    # Login y logout personalizados
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]