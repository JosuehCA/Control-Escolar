from django.urls import path

from .. import views
from sistema.views import views_autenticacion

urlpatterns = [
    path("", views.indice, name="indice"),
    path("iniciarSesion", views_autenticacion.iniciarSesion, name="iniciar_sesion"),
    path("cerrarSesion", views_autenticacion.cerrarSesion, name="cerrar_sesion"),
    path("registrarse", views_autenticacion.registrarse, name="registrarse")
]