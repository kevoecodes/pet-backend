from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class PetTrackChannel:
    def __init__(self, data):
        self.channel_name, self.data = 'pet_location', {"pet_location": data}
        self.__post_to_channel()

    def __post_to_channel(self):
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            self.channel_name,
            {
                "type": "send.message",
                "data": self.data,
            }
        )
