from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/mensajes/', consumers.MensajeConsumer.as_asgi()),
]
