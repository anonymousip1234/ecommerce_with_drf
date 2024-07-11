from django.urls import re_path
from .consumers import SKUCountConsumer

websocket_urlpatterns = [
    re_path(r'ws/sold_skus/$', SKUCountConsumer.as_asgi()),
]
