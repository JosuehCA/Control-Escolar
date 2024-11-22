import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any
from sistema.models.models_mensajeria import MensajePrivado, MensajeGrupal, MensajeGeneral, MensajeBase
from sistema.models.models import Grupo, UsuarioEscolar
from datetime import datetime
from abc import ABC, abstractmethod
from asgiref.sync import sync_to_async

class ConsumidorWebSocketBase(ABC, AsyncWebsocketConsumer):
    '''Clase abstracta para consumidores de mensajes WebSocket. Nota: Los consumidores directos deben heredar de AsyncWebsocketConsumer.'''
    canalWebSocket: str
    mensaje: MensajeBase

    @abstractmethod
    def crearInstanciaDeMensaje(self) -> None:
        pass

    @abstractmethod
    async def definirCanalWebSocket(self) -> None:
        pass

    @abstractmethod
    async def recibirMensajeDeCanal(self, datosJSON: str) -> dict:
        pass

    @abstractmethod
    async def manejarEventoMensaje(self, eventoDatos: dict) -> None:
        pass

    async def guardarMensajeEnBaseDeDatos(self, datosDeMensajeAGuardar: dict) -> None:
        await sync_to_async(self.mensaje.recibirDatosDeMensajeEnDiccionario)(datosDeMensajeAGuardar)
        await sync_to_async(self.mensaje.almacenarEnBaseDeDatos)()

    async def desconectarUsuarioDeCanal(self) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.canalWebSocket,
            self.channel_name
        )

    async def connect(self) -> None:
        """Conecta al usuario al grupo WebSocket segun la configuracion."""
        await self.definirCanalWebSocket()
        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Desconecta al usuario del grupo WebSocket."""
        await self.desconectarUsuarioDeCanal()

    async def receive(self, text_data):
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensajeRecibido: dict = await self.recibirMensajeDeCanal(text_data)
        await self.crearInstanciaDeMensaje()
        await self.guardarMensajeEnBaseDeDatos(datosDeMensajeRecibido)
        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'manejarEventoMensaje',
                'mensaje': self.mensaje
            }
        )

class MensajePrivadoConsumidor(ConsumidorWebSocketBase, AsyncWebsocketConsumer):

    nombreConexion: str

    async def crearInstanciaDeMensaje(self) -> None:
        """Define el tipo de mensaje a manejar."""
        self.mensaje = MensajePrivado()

    async def definirCanalWebSocket(self) -> None:
        """Conecta al usuario al grupo WebSocket."""
        self.nombreConexion = self.scope['url_route']['kwargs']['nombreConexion']
        self.canalWebSocket = f'conversacion_privada_{self.nombreConexion}'

    async def recibirMensajeDeCanal(self, datosJSON: str) -> dict:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal:UsuarioEscolar = self.scope['user']
        receptorUsuario: UsuarioEscolar = await sync_to_async(UsuarioEscolar.obtenerUsuarioSegunNombreDeUsuario)(datosDeMensaje['nombreReceptor'])

        return {
            'emisorUsuario': usuarioCanal,
            'receptorUsuario': receptorUsuario,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje']
        }

    async def manejarEventoMensaje(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajePrivado: MensajePrivado = eventoDatos['mensaje']

        await self.send(text_data=json.dumps({
            'emisor': mensajePrivado.emisorUsuario.username,
            'contenido': mensajePrivado.contenidoMensaje,
            'fecha': mensajePrivado.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))

class MensajeGrupalConsumidor(ConsumidorWebSocketBase, AsyncWebsocketConsumer):

    grupoReceptor: str

    async def crearInstanciaDeMensaje(self) -> None:
        """Define el tipo de mensaje a manejar."""
        self.mensaje = MensajeGrupal()

    async def definirCanalWebSocket(self) -> None:
        """Conecta al usuario al grupo WebSocket grupal."""
        self.grupoReceptor = self.scope['url_route']['kwargs']['grupoReceptor']
        self.canalWebSocket = f'conversacion_grupal_'+ self.grupoReceptor

    async def recibirMensajeDeCanal(self, datosJSON: str) -> dict:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal:UsuarioEscolar = self.scope['user']
        grupo = await sync_to_async(Grupo.obtenerGrupoSegunNombre)(self.grupoReceptor)
        return {
            'emisorUsuario': usuarioCanal,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje'],
            'grupoRelacionado': grupo
        }

    async def manejarEventoMensaje(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajeGrupal: MensajeGrupal = eventoDatos['mensaje']  # Obtener la instancia de MensajeGrupal

        await self.send(text_data=json.dumps({
            'emisor': mensajeGrupal.emisorUsuario.username,
            'contenido': mensajeGrupal.contenidoMensaje,
            'fecha': mensajeGrupal.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))


class MensajeGeneralConsumidor(ConsumidorWebSocketBase, AsyncWebsocketConsumer):

    async def crearInstanciaDeMensaje(self) -> None:
        """Define el tipo de mensaje a manejar."""
        self.mensaje = MensajeGeneral()

    async def definirCanalWebSocket(self) -> None:
        """Conecta al usuario al grupo WebSocket general."""
        print("Conectando usuario al canal general")
        self.canalWebSocket = f'conversacion_general'

    async def recibirMensajeDeCanal(self, datosJSON: str) -> dict:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal: UsuarioEscolar = self.scope['user']

        return {
            'emisorUsuario': usuarioCanal,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje'],
        }

    async def manejarEventoMensaje(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajeGeneral: MensajeGrupal = eventoDatos['mensaje']  # Obtener la instancia de MensajeGeneral

        await self.send(text_data=json.dumps({
            'emisor': mensajeGeneral.emisorUsuario.username,
            'contenido': mensajeGeneral.contenidoMensaje,
            'fecha': mensajeGeneral.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))