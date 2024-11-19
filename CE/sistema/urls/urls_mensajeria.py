from django.urls import path

from sistema.views import views_mensajeria

urlpatterns = [
    path("mensajeria", views_mensajeria.enviarMensajeDirecto, name="mensaje_directo")
]
