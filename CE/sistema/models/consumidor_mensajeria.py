import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any

# Consumidor de WebSocket para la mensajería
class MensajeConsumidor(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        """Conecta al usuario al grupo WebSocket."""
        self.nombreGrupoUsuario = f'chat_{self.scope["user"].id}'

        # Unir al grupo WebSocket del usuario
        await self.channel_layer.group_add(
            self.nombreGrupoUsuario,
            self.channel_name
        )
        await self.accept()

        print(f'Conexión establecida: {self.nombreGrupoUsuario}')

    async def disconnect(self, codigoCerrar: int) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.nombreGrupoUsuario,
            self.channel_name
        )

        print(f'Conexión cerrada: {self.nombreGrupoUsuario}')

    async def receive(self, text_data: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        # Deserializa el mensaje en JSON
        datosJson: dict = json.loads(text_data)
        contenidoMensaje: str = datosJson['mensaje']

        print(f'Mensaje recibido: {contenidoMensaje}')

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

        print(f'Mensaje enviado: {contenidoMensaje}')