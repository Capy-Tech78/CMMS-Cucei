from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_equipos, name='lista_equipos'),  # 👈 la raíz del sitio mostrará la lista
]
