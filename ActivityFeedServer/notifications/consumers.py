import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model


async def get_user_from_token(token):
    User = get_user_model()
    try:
        secret_key = settings.SECRET_KEY
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        uid = decoded_token["user_id"]
        user = await database_sync_to_async(User.objects.get)(pk=uid)
        return user
    except (jwt.DecodeError, User.DoesNotExist):
        return None


class TokenAuthMiddleware(BaseMiddleware):
    def fetch_token_from_header(self, headers):
        items = {key.decode(): value.decode() for key, value in headers}
        if "authorization" in items:
            return items["authorization"].split(" ")[1]
        return None

    async def __call__(self, scope, receive, send):
        # Authenticate the WebSocket request using the provided token
        # You can use the `get_user()` function or any other authentication mechanism
        # and set the authenticated user in the scope["user"] attribute.

        token = self.fetch_token_from_header(scope["headers"])
        if token is None:
            return
        else:
            user = await get_user_from_token(token)
            scope["user"] = user

            # Call the next middleware/consumer in the stack
            return await super().__call__(scope, receive, send)


class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if (
            "user" not in self.scope
            or self.scope["user"] is None
            or self.scope["user"].is_anonymous
        ):
            # Reject the connection if the user is not authenticated
            await self.close()
        else:
            self.project_id = self.scope["url_route"]["kwargs"]["project_id"]
            self.room_group_name = "project_%s" % self.project_id

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if (
            "user" not in self.scope
            or self.scope["user"] is None
            or self.scope["user"].is_anonymous
        ):
            # Reject the connection before creating itself
            return
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # You can handle incoming messages here if needed
        pass

    async def send_file_edit(self, event):
        # Send file edit event to the WebSocket
        await self.send(text_data=event["text"])
