from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from ticket.consumers import UpdateConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/updates/", UpdateConsumer.as_asgi()),
                ]
            )
        ),
    }
)
