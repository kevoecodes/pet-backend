from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from pets_management.models import Pet
from pets_management.serializers import PetsListSerializer


class PetTrackConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.tickets = []
        self.thread_name = None
        self.apos_id = None

    async def websocket_connect(self, event):
        self.thread_name = "pet_location"
        await self.channel_layer.group_add(
            self.thread_name,
            self.channel_name
        )
        await self.accept()


    async def websocket_receive(self, event):
        print("Message: ", event['text'])

        await self.channel_layer.group_send(
            self.thread_name,
            {
                "type": "send.message",
                "data": event['text']
            }
        )

    async def send_message(self, event):
        print('messages', event)

        await self.send_json(event['data'])

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.channel_layer.group_discard(
            self.thread_name,
            self.channel_name
        )
        await self.disconnect(event['code'])
        raise StopConsumer()


class SystemPetTrackerConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.pets = []
        self.thread_name = None
        self.apos_id = None

    async def websocket_connect(self, event):
        self.thread_name = "system_tracker"
        await self.channel_layer.group_add(
            self.thread_name,
            self.channel_name
        )
        await self.accept()
        await self.pets_outside_fence()
        for pet in self.pets:
            await self.send_json({
                "type": "pet_outside_boundary",
                "pet": pet
            })

    async def websocket_receive(self, event):
        print("Message: ", event['text'])

        await self.channel_layer.group_send(
            self.thread_name,
            {
                "type": "send.message",
                "data": event['text']
            }
        )

    async def send_message(self, event):
        print('messages', event)

        await self.send_json(event['data'])

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.channel_layer.group_discard(
            self.thread_name,
            self.channel_name
        )
        await self.disconnect(event['code'])
        raise StopConsumer()

    @database_sync_to_async
    def pets_outside_fence(self):
        self.pets = PetsListSerializer(instance=Pet.filter_outside_fence(), many=True).data
