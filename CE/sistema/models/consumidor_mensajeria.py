import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Any
from sistema.models.models_mensajeria import MensajePrivado, MensajeGrupal, MensajeGeneral
from sistema.models.models import Grupo, UsuarioEscolar
from datetime import datetime
from abc import ABC, abstractmethod
from asgiref.sync import sync_to_async

def obtenerInstanciaDeGrupoSegunNombre(nombreGrupo: str) -> Grupo:
    """Obtiene una instancia de Grupo según el nombre del grupo."""
    return Grupo.objects.get(nombre=nombreGrupo)

def obtenerInstanciaDeUsuarioEscolarSegunNombre(nombreUsuario: str) -> UsuarioEscolar:
    """Obtiene una instancia de UsuarioEscolar según el nombre de usuario."""
    return UsuarioEscolar.objects.get(username=nombreUsuario)

class ConsumidorBase(ABC):
    '''Clase abstracta para consumidores de mensajes WebSocket. Nota: Los consumidores directos deben heredar de AsyncWebsocketConsumer.'''
    @abstractmethod
    async def conectarUsuarioACanal(self):
        pass

    @abstractmethod
    async def recibirDeCanal(self, datosJSON: str):
        pass

    async def desconectarUsuarioDeCanal(self) -> None:
        """Desconecta al usuario del grupo WebSocket."""
        await self.channel_layer.group_discard(
            self.canalWebSocket,
            self.channel_name
        )

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

    nombreConexion: str

    async def conectarUsuarioACanal(self) -> None:
        """Conecta al usuario al grupo WebSocket."""
        self.nombreConexion = self.scope['url_route']['kwargs']['nombreConexion']
        self.canalWebSocket = f'conversacion_privada_{self.nombreConexion}'

        # Unir al grupo WebSocket del usuario
        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()

        print(f'Conexión privada establecida: {self.canalWebSocket}')

    async def recibirDeCanal(self, datosJSON: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal = self.scope['user']
        receptorUsuario = await sync_to_async(obtenerInstanciaDeUsuarioEscolarSegunNombre)(datosDeMensaje['nombreReceptor'])
        instanciaMensajePrivado = MensajePrivado()
        datosDeMensajePrivado = {
            'emisorUsuario': usuarioCanal,
            'receptorUsuario': receptorUsuario,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje']
        }
        instanciaMensajePrivado.recibirDatosDeMensajeEnDiccionario(datosDeMensajePrivado)
        await sync_to_async(instanciaMensajePrivado.almacenarEnBaseDeDatos)()

        # Envía el mensaje al grupo WebSocket
        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'eventoMensajePrivado',
                'mensaje': instanciaMensajePrivado
            }
        )

    async def eventoMensajePrivado(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajePrivado = eventoDatos['mensaje']
        await self.send(text_data=json.dumps({
            'emisor': mensajePrivado.emisorUsuario.username,
            'contenido': mensajePrivado.contenidoMensaje,
            'fecha': mensajePrivado.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))

class MensajeGrupalConsumidor(ConsumidorBase, AsyncWebsocketConsumer):

    grupoReceptor: str

    async def conectarUsuarioACanal(self) -> None:
        """Conecta al usuario al grupo WebSocket grupal."""
        self.grupoReceptor = self.scope['url_route']['kwargs']['grupoReceptor']
        self.canalWebSocket = f'conversacion_grupal_'+ self.grupoReceptor

        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()
        print(f'Conexión grupal establecida: {self.canalWebSocket}')

    async def recibirDeCanal(self, datosJSON: str) -> None:
        """Recibe un mensaje en formato JSON a través de WebSocket."""
        datosDeMensaje: dict = json.loads(datosJSON)
        usuarioCanal = self.scope['user']
        grupo = await sync_to_async(obtenerInstanciaDeGrupoSegunNombre)(self.grupoReceptor)
        instanciaMensajeGrupal = MensajeGrupal()
        datosDeMensajeGrupal = {
            'emisorUsuario': usuarioCanal,
            'contenidoMensaje': datosDeMensaje['contenidoMensaje'],
            'grupoRelacionado': grupo
        }
        instanciaMensajeGrupal.recibirDatosDeMensajeEnDiccionario(datosDeMensajeGrupal)
        await sync_to_async(instanciaMensajeGrupal.almacenarEnBaseDeDatos)()

        await self.channel_layer.group_send(
            self.canalWebSocket,
            {
                'type': 'eventoMensajeGrupal',
                'mensaje': instanciaMensajeGrupal
            }
        )
        print(f'Mensaje recibido: {datosDeMensaje}')

    async def eventoMensajeGrupal(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajeGrupal = eventoDatos['mensaje']  # Obtener la instancia de MensajeGrupal

        await self.send(text_data=json.dumps({
            'emisor': mensajeGrupal.emisorUsuario.username,
            'contenido': mensajeGrupal.contenidoMensaje,
            'fecha': mensajeGrupal.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))
        print(f'Mensaje enviado: {mensajeGrupal.contenidoMensaje}')


class MensajeGeneralConsumidor(ConsumidorBase, AsyncWebsocketConsumer):

    async def conectarUsuarioACanal(self) -> None:
        """Conecta al usuario al grupo WebSocket general."""
        print("Conectando usuario al canal general")
        self.canalWebSocket = f'conversacion_general'

        await self.channel_layer.group_add(
            self.canalWebSocket,
            self.channel_name
        )
        await self.accept()

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
        print(f'Mensaje general recibido: {datosDeMensaje}')

    async def eventoMensajeGeneral(self, eventoDatos: dict) -> None:
        """Envía el mensaje recibido a través de WebSocket."""
        mensajeGeneral = eventoDatos['mensaje']  # Obtener la instancia de MensajeGeneral

        await self.send(text_data=json.dumps({
            'emisor': mensajeGeneral.emisorUsuario.username,
            'contenido': mensajeGeneral.contenidoMensaje,
            'fecha': mensajeGeneral.fechaEnviado.strftime('%Y-%m-%d %H:%M:%S')
        }))

        print(f'Mensaje enviado: {mensajeGeneral.contenidoMensaje}')