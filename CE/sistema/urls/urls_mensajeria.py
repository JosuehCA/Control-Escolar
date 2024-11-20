from django.urls import path

from sistema.views.views_mensajeria import mostrarVistaConversacion

urlpatterns = [
    path("<str:servicioDeMensajeriaURL>", mostrarVistaConversacion, name="conversacion"),
]
