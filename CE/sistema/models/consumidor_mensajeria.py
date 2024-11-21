import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any
from sistema.models.models_mensajeria import MensajeDirecto, MensajeGrupo, MensajeGeneral
from datetime import datetime
from abc import ABC, abstractmethod

class ConsumidorBase(AsyncWebsocketConsumer, ABC):
    @abstractmethod
    async def conectarUsuarioACanal(self):
        pass

    @abstractmethod
    async def desconectarUsuarioDeCanal(self):
        pass

    @abstractmethod
    async def recibirDeCanal(self, text_data):
        pass

    async def connect(self):
        self.conectarUsuarioACanal()

    async def disconnect(self, close_code):
        self.desconectarUsuarioDeCanal()

    async def receive(self, text_data):
        self.recibirDeCanal(text_data)

class MensajePrivadoConsumidor(ConsumidorBase):

    async def connect(self) -> None:
        """Conecta al usuario al grupo WebSocket."""
        self.canalWebSocket = f'conversacion_privada_{self.scope["url_route"]["kwargs"]["nombreDeUsuarioReceptor"]}'

        # Unir al grupo WebSocket del usuario
        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()

        print(f'Conexión establecida: {self.canalWebSocket}')

    async def disconnect(self, codigoCerrar: int) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.canalWebSocket,
            self.channel_name
        )

        print(f'Conexión cerrada: {self.canalWebSocket}')

    async def receive(self, text_data: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosJson: dict = json.loads(text_data)
        emisorUsuario = datosJson['emisor']
        contenidoMensaje = datosJson['contenido']
        fechaEnviado = datosJson['fecha']

        # Guarda el mensaje en la base de datos
        mensaje = Mensaje(emisor=emisor, contenido=contenido, fecha=fecha)
        mensaje.save()
        print(f'Mensaje recibido: {contenidoMensaje}')

        # Envía el mensaje al grupo WebSocket
        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'eventoMensajeGrupo',
                'mensaje': datosJson
            }
        )

    async def eventoMensajeGrupo(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajeJSON: str = eventoDatos['mensaje']
        await self.send(text_data=json.dumps({
            'mensaje': mensajeJSON
        }))

        print(f'Mensaje enviado: {mensajeJSON}')

class MensajeGrupalConsumidor(ConsumidorBase):
    async def connect(self) -> None:
        pass

    async def disconnect(self, close_code: int) -> None:
        pass
    async def receive(self, text_data: str) -> None:
        pass

class MensajeGeneralConsumidor(ConsumidorBase):

    mensajerGeneralInstancia = MensajeGeneral()

    async def conectarUsuarioACanal(self) -> None:
        """Conecta al usuario al grupo WebSocket general."""
        print('Conexión establecida: conversacion_general')
        self.canalWebSocket = f'conversacion_general'

        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()

    async def desconectarUsuarioDeCanal(self) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.canalWebSocket,
            self.channel_name
        )

    async def recibirDeCanal(self, datosJSON: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)

        self.mensajerGeneralInstancia.diccionarioAMensaje(datosDeMensaje)
        self.mensajerGeneralInstancia.almacenarEnBaseDeDatos()

        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'eventoMensajeGeneral',
                'mensaje': datosDeMensaje
            }
        )

    async def eventoMensajeGeneral(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        datosDeMensaje: dict = eventoDatos['mensaje']
        await self.send(text_data=json.dumps({
        'emisor': datosDeMensaje['emisorUsuario'],
        'contenido': datosDeMensaje['contenidoMensaje'],
        'fecha': datosDeMensaje['fechaEnviado']
        }))

        print(f'Mensaje enviado: {datosDeMensaje}')