from django.urls import path
from . import consumers_msj

websocket_urlpatterns = [
    path('ws/mensajes/', consumers_msj.MensajeConsumer.as_asgi()),
]
