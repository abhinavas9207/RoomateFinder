import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, ChatMessage


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        # ❌ Reject unauthenticated users
        if self.scope["user"] is None or isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        # ❌ Reject invalid chat
        try:
            chat = await database_sync_to_async(ChatRoom.objects.get)(id=self.chat_id)
        except ChatRoom.DoesNotExist:
            await self.close()
            return

        # 🔐 Check user is participant
        participants = await database_sync_to_async(list)(chat.participants.all())
        if self.scope["user"] not in participants:
            await self.close()
            return

        self.group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        sender = self.scope["user"]

        chat = await database_sync_to_async(ChatRoom.objects.get)(id=self.chat_id)

        # ✅ Save message
        await database_sync_to_async(ChatMessage.objects.create)(
            chat=chat,
            sender=sender,
            message=message
        )

        # ✅ Broadcast message
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
