from django.urls import path

from sistema.views.views_mensajeria import mostrarVistaConversacionGeneral, mostrarVistaConversacionGrupal, mostrarVistaConversacionPrivada

urlpatterns = [
    path("privada/<str:nombreDeUsuarioReceptor>", mostrarVistaConversacionPrivada, name="conversacion"),
    path("grupal/<str:grupoReceptor>", mostrarVistaConversacionGrupal, name="conversacionGrupal"),
    path("general", mostrarVistaConversacionGeneral, name="conversacionGeneral"),
]
