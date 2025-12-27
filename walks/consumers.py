from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, LiveLocation, ScheduledWalks
from accounts.models import *
from channels.db import database_sync_to_async
import time
from asgiref.sync import async_to_sync
from fcm.send_notification import sendNotifications

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
                await self.send_json({"error": "User not found"})
                return

           
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "location_update",
                    "user_id": user_id,
                    "latitude": lat,
                    "longitude": lon,
                }
            )
            
        elif action == "status_update":

            user_id = data.get("user_id")
            location_sharing = data["location_sharing"]
            request_complete = data["request_complete"]
            accept_complete_walk = data["accept_complete_walk"]
            reject_complete_walk = data["reject_complete_walk"]
            room_id = data["room_id"]

            if not user_id:
                await self.send_json({"error": "User not found"})
                return
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "status_update",
                    "user_id": user_id,
                    "location_sharing":location_sharing,
                    "request_complete":request_complete,
                    "reject_complete_walk":reject_complete_walk
                }
            )

            if accept_complete_walk:
                completed = await complete_walk(room_id)

                if completed:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "walk_completed"
                        }
                    )


    async def location_update(self, event):
        print(event)
        await self.send_json({
            "event": "location_update",
            "user_id": event["user_id"],
            "latitude": event["latitude"],
            "longitude": event["longitude"],
        })
        return True

    async def status_update(self, event):
        print(event)
        await self.send_json({
            "event": "status_update",
            "user_id": event["user_id"],
            "location_sharing":event["location_sharing"],
            "request_complete": event["request_complete"],
            "reject_complete_walk": event["reject_complete_walk"]
        })
        return True
    
    async def walk_completed(self,event):
        await self.send_json({
            "event":"walk_completed"
        })

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))

@database_sync_to_async
def complete_walk(room_id):
    try:
        walk = ScheduledWalks.objects.get(room__id=room_id)

        if walk.walk_completed:
            return True

        walk.walk_completed = True

        # Update stats
        walk.walker.total_walks += 1
        walk.wanderer.total_walks += 1
        walk.room.completed = True
        walk.room.save()
        walk.walker.save()
        walk.wanderer.save()
        walk.save()

        return True

    except ScheduledWalks.DoesNotExist:
        return False
        
    except Exception as e:
        return False