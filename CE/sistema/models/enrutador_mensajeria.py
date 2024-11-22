from django.urls import path
from .consumidor_mensajeria import MensajeGeneralConsumidor, MensajeGrupalConsumidor, MensajePrivadoConsumidor
 
websocket_urlpatterns = [
    path('ws/mensajeria/privada/<str:nombreConexion>', MensajePrivadoConsumidor.as_asgi()),
    path('ws/mensajeria/grupal/<str:grupoReceptor>', MensajeGrupalConsumidor.as_asgi()),
    path('ws/mensajeria/general', MensajeGeneralConsumidor.as_asgi()),
]
