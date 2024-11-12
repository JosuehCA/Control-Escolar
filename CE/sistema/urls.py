from django.urls import path

from . import views

urlpatterns = [
    path("", views.indice, name="indice"),
    path("iniciarSesion", views.iniciarSesion, name="iniciar_sesion"),
    path("cerrarSesion", views.cerrarSesion, name="cerrar_sesion"),
    path("registrarse", views.registrarse, name="registrarse"),
<<<<<<< HEAD
    path("mensajeria", views.enviarMensajeDirecto, name="mensaje_directo")
=======
    path("generarReporte", views.generarReporte, name="generar_reporte")
>>>>>>> a0b7ab7 (Se añadió archivo de dependencias necesarias. Ir agregando a medida que se necesiten más)
]
