import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()
        await self.set_online(True)
        await self.broadcast_status("online")
        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connected to OCALL"
        }))
    async def disconnect(self, close_code):
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(self.user_group, self.channel_name)
        if hasattr(self, "user") and not self.user.is_anonymous:
            await self.set_online(False)
            await self.broadcast_status("offline")
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        message_type = data.get("type")
        if message_type == "heartbeat":
            await self.set_online(True)
            return
        target_user_id = data.get("target_user_id")
        if not target_user_id:
            return
        target_group = f"user_{target_user_id}"
        data["sender_id"] = self.user.id
        data["sender_name"] = self.user.username
        await self.channel_layer.group_send(
            target_group,
            {
                "type": "forward_message",
                "data": data
            }
        )
    async def forward_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def broadcast_status(self, status):
        await self.channel_layer.group_send(
            "online_status",
            {
                "type": "user_status",
                "user_id": self.user.id,
                "status": status
            }
        )
    async def user_status(self, event):
        if event["user_id"] != self.user.id:
            await self.send(text_data=json.dumps({
                "type": "user-status",
                "user_id": event["user_id"],
                "status": event["status"]
            }))
    @database_sync_to_async
    def set_online(self, status):
        profile = self.user.profile
        profile.is_online = status
        profile.save(update_fields=["is_online"])