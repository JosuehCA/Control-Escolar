import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any

# Consumidor de WebSocket para la mensajería
class MensajeConsumidor(AsyncWebsocketConsumer):
    async def conectarUsuario(self) -> None:
        """Conecta al usuario al grupo WebSocket."""
        self.nombreGrupoUsuario = f'chat_{self.scope["user"].id}'

        # Unir al grupo WebSocket del usuario
        await self.channel_layer.group_add(
            self.nombreGrupoUsuario,
            self.channel_name
        )
        await self.accept()

    async def desconectarUsuario(self, codigoCerrar: int) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.nombreGrupoUsuario,
            self.channel_name
        )

    async def recibirMensajeWebSocket(self, textoDatos: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        # Deserializa el mensaje en JSON
        datosJson: dict = json.loads(textoDatos)
        contenidoMensaje: str = datosJson['mensaje']

        # Envía el mensaje al grupo WebSocket
        await self.channel_layer.group_send(
            self.nombreGrupoUsuario,
            {
                'type': 'eventoMensajeGrupo',
                'mensaje': contenidoMensaje
            }
        )

    async def eventoMensajeGrupo(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        contenidoMensaje: str = eventoDatos['mensaje']
        await self.send(text_data=json.dumps({
            'mensaje': contenidoMensaje
        }))