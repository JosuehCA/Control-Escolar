import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MensajeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'chat_%s' % self.scope['user'].id  # Identificador único del usuario

        # Unir al grupo de WebSockets del usuario
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Recibe un mensaje del WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Enviar el mensaje a todos los usuarios del grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'mensaje_evento',
                'message': message
            }
        )

    # Recibe un mensaje desde el grupo de WebSocket
    async def mensaje_evento(self, event):
        message = event['message']

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
