from django.urls import path
from . import consumers_msj

websocket_urlpatterns = [
    path('ws/mensajes/', consumers_msj.MensajeConsumidor.as_asgi()),
]
