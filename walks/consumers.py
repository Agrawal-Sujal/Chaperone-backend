from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, LiveLocation
from accounts.models import *
from channels.db import database_sync_to_async
import time

class LocationChannel(AsyncWebsocketConsumer):

    async def connect(self):

    
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"location_{self.room_name}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send_json({
            "message": f"Connected to room {self.room_name}"
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "update_location":

            user_id = data.get("user_id")
            lat = data["latitude"]
            lon = data["longitude"]

            if not user_id:
                await self.send_json({"error": "User Id not found"})
                return

            success, msg = await self.save_location(user_id, self.room_name, lat, lon)
            if not success:
                await self.send_json({"error": msg})
                return

            # Broadcast location to everyone in the same room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "location_update",
                    "user_id": user_id,
                    "latitude": lat,
                    "longitude": lon,
                }
            )

    async def location_update(self, event):
        # print(event)
        await self.send_json({
            "event": "location_update",
            "user_id": event["user_id"],
            "latitude": event["latitude"],
            "longitude": event["longitude"],
        })
    from asgiref.sync import sync_to_async

    @sync_to_async
    def save_location(self, user_id, room_name, lat, lon):
        

        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_name)

        # print(user_id)
        if user.is_walker:
            if room.walker.user != user:
                return False,"Room already full"
        else :
            if room.wanderer.user != user:
                return False,"Room already full"
            
        loc,_ = LiveLocation.objects.get_or_create(room=room,user = user)

        
        loc.longitude = lon
        loc.latitude = lat

        loc.save()

        return True, "Location saved."

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))



# @database_sync_to_async
# def get_or_create_room(name):
#     return Room.objects.get_or_create(name=name)
