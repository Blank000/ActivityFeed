from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Action
from .serializers import ActionSerializer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = 'project_%s' % self.project_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # You can handle incoming messages here if needed
        pass

    async def send_file_edit(self, event):
        # Send file edit event to the WebSocket
        await self.send(text_data=event['text'])

        # Record the action in the database
        action_data = event['action_data']
        await self.save_action(action_data)

    @database_sync_to_async
    def save_action(self, data):
        serializer = ActionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

