import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Consumidor de WebSocket para la mensajería
class MensajeConsumidor(AsyncWebsocketConsumer):
    async def ConectarUsuario(self):
        # Identificador único para cada usuario en WebSocket
        self.NombreGrupoUsuario = 'chat_%s' % self.scope['user'].id

        # Unir al grupo WebSocket del usuario
        await self.channel_layer.group_add(
            self.NombreGrupoUsuario,
            self.channel_name
        )
        await self.accept()

    async def DesconectarUsuario(self, CodigoCerrar):
        # Remueve al usuario del grupo WebSocket al desconectarse
        await self.channel_layer.group_discard(
            self.NombreGrupoUsuario,
            self.channel_name
        )

    async def RecibirMensajeWebSocket(self, TextoDatos):
        # Deserializa el mensaje en JSON
        DatosJson = json.loads(TextoDatos)
        ContenidoMensaje = DatosJson['mensaje']

        # Envía el mensaje al grupo WebSocket
        await self.channel_layer.group_send(
            self.NombreGrupoUsuario,
            {
                'type': 'EventoMensajeGrupo',
                'mensaje': ContenidoMensaje
            }
        )

    async def EventoMensajeGrupo(self, EventoDatos):
        # Extrae el mensaje y lo envía al WebSocket
        ContenidoMensaje = EventoDatos['mensaje']
        await self.send(text_data=json.dumps({
            'mensaje': ContenidoMensaje
        }))