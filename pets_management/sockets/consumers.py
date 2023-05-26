from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


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

