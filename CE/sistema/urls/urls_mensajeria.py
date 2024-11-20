from django.urls import path

from sistema.views import views_mensajeria

urlpatterns = [
    path("/<str:servicioDeMensajeriaURL>", views.mostrarVistaConversacion, name="conversacion"),
]
