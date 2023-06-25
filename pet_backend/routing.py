from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from pets_management.sockets.consumers import PetTrackConsumer, SystemPetTrackerConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r"^ws/ws-pet-tracker", PetTrackConsumer.as_asgi()),
                re_path(r"^ws/ws-system-tracker", SystemPetTrackerConsumer.as_asgi()),
            ]
        )
    )
})
