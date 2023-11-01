from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import Message_App.routing

application = ProtocolTypeRouter({
     'websocket': AuthMiddlewareStack(
          URLRouter(
               Message_App.routing.websocket_urlpatterns
          )
     ),
})