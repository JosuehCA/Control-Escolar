from django.urls import path
from . import consumidor_mensajeria
 
websocket_urlpatterns = [
    path('ws/mensajeria/<str:servicioDeMensajeriaURL>', consumidor_mensajeria.MensajeConsumidor.as_asgi()),
]
