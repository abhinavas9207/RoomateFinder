from django.urls import path
from .consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', PrivateChatConsumer.as_asgi()),
]
