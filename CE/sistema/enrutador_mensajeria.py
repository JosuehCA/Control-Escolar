from django.urls import path
from . import consumers_msj
 
websocket_urlpatterns = [
    path('ws/mensajeria/<str:servicioDeMensajeriaURL>', consumers_msj.MensajeConsumidor.as_asgi()),
]
