from django.urls import path
from . import consumidor_mensajeria
 
websocket_urlpatterns = [
    path('ws/mensajeria/privado/<str:nombreDeUsuarioReceptor>', consumidor_mensajeria.MensajePrivadoConsumidor.as_asgi()),
    path('ws/mensajeria/grupal/<str:grupoReceptor>', consumidor_mensajeria.MensajeGrupalConsumidor.as_asgi()),
    path('ws/mensajeria/general', consumidor_mensajeria.MensajeGeneralConsumidor.as_asgi()),
]
