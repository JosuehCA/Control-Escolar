import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any
from sistema.models.models_mensajeria import MensajeDirecto, MensajeGrupo, MensajeGeneral
from datetime import datetime
from abc import ABC, abstractmethod
from asgiref.sync import sync_to_async

class ConsumidorBase(ABC):
    '''Clase abstracta para consumidores de mensajes WebSocket. Nota: Los consumidores directos deben heredar de AsyncWebsocketConsumer.'''
    @abstractmethod
    async def conectarUsuarioACanal(self):
        pass

    @abstractmethod
    async def desconectarUsuarioDeCanal(self):
        pass

    @abstractmethod
    async def recibirDeCanal(self, text_data):
        pass

    async def connect(self) -> None:
        """Conecta al usuario al grupo WebSocket general."""
        await self.conectarUsuarioACanal()

    async def disconnect(self, close_code):
        """Desconecta al usuario del grupo WebSocket."""
        await self.desconectarUsuarioDeCanal()

    async def receive(self, text_data):
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        await self.recibirDeCanal(text_data)

class MensajePrivadoConsumidor(ConsumidorBase, AsyncWebsocketConsumer):

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

class MensajeGrupalConsumidor(ConsumidorBase, AsyncWebsocketConsumer):
    async def connect(self) -> None:
        pass

    async def disconnect(self, close_code: int) -> None:
        pass
    async def receive(self, text_data: str) -> None:
        pass

class MensajeGeneralConsumidor(ConsumidorBase, AsyncWebsocketConsumer):

    mensajerGeneralInstancia = MensajeGeneral()

    async def conectarUsuarioACanal(self) -> None:
        """Conecta al usuario al grupo WebSocket general."""
        print("Conectando usuario al canal general")
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
        print("Desconectando usuario del canal general")

    async def recibirDeCanal(self, datosJSON: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal = self.scope['user']
        instanciaMensajeGeneral = MensajeGeneral()
        datosDeMensajeGeneral ={
            'emisorUsuario': usuarioCanal,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje'],
        }
        instanciaMensajeGeneral.recibirDatosDeMensajeEnDiccionario(datosDeMensajeGeneral)
        await sync_to_async(instanciaMensajeGeneral.almacenarEnBaseDeDatos)()

        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'eventoMensajeGeneral',
                'mensaje': instanciaMensajeGeneral
            }
        )
        print(f'Mensaje recibido: {datosDeMensaje}')

    async def eventoMensajeGeneral(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensaje = eventoDatos['mensaje']  # Obtener la instancia de MensajeGeneral

        await self.send(text_data=json.dumps({
            'emisor': mensaje.emisorUsuario.username,
            'contenido': mensaje.contenidoMensaje,
            'fecha': mensaje.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))

        print(f'Mensaje enviado: {mensaje.contenidoMensaje}')