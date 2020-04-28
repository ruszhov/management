from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, include

from channels.routing import ProtocolTypeRouter
import parsing.consumers as parsing_consumers

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
# })

websocket_urlpatterns = [
    re_path(r'ws/parsing/parse/$', parsing_consumers.ParsingConsumer, name='parsing-consumer'),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})