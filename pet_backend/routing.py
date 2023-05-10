from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                # re_path(r"^ws/ws-office-stats/(?P<office_id>)", OfficeStatsConsumer.as_asgi()),
            ]
        )
    )
})
