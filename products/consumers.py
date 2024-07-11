import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SKUCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "sku_counts",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "sku_counts",
            self.channel_name
        )

    async def receive(self, text_data):
        pass  # Not needed for this implementation

    async def sku_count_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'sku_count_update',
            'data': event['data']
        }))
