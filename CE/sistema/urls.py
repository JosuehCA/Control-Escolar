from django.urls import path

from . import views

urlpatterns = [
    path("", views.indice, name="indice"),
    path("iniciarSesion", views.iniciarSesion, name="iniciar_sesion"),
    path("cerrarSesion", views.cerrarSesion, name="cerrar_sesion"),
    path("registrarse", views.registrarse, name="registrarse"),
    path("mensajeria", views.enviarMensajeDirecto, name="mensaje_directo"),
    path("generarReporte", views.generarReporte, name="generar_reporte"),
    path("generarDiagramaPastel", views.generarDiagramaPastel, name="generar_diagrama_pastel")
]
