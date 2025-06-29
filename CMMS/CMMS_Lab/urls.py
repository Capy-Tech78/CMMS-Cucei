""""
from django.urls import path
from . import views

urlpatterns = [
    path('hola/', views.hola, name='hola'),
]
"""
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.lista_equipos, name='lista_equipos'),
    path('registrar/', views.registrar_equipo, name='registrar_equipo'),

    # Login y logout personalizados
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
