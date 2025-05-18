import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("trade_group", self.channel_name)
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("trade_group", self.channel_name)
        print("WebSocket disconnected")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            master = data.get('master_account')

            if action in (['open_trade', 'modify_trade', 'close_trade', 'open_pending_order']) and (master == 'soheilmaster'):
                await self.channel_layer.group_send(
                    "trade_group",
                    {
                        'type': 'broadcast_message',
                        'message': data
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid action type and master'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Unexpected error: {str(e)}'
            }))

    async def broadcast_message(self, event):
        message = event.get('message')
        action = message.get('action')


        if action == 'open_trade':
            print(f"[INFO] Broadcasting open_trade: {message}")
        elif action == 'modify_trade':
            print(f"[INFO] Broadcasting modify_trade: {message}")
        elif action == 'close_trade':
            print(f"[INFO] Broadcasting close_trade: {message}")
        elif action == 'open_pending_order':
            print(f"[INFO] Broadcasting open_pending_order: {message}")
        else:
            print(f"[WARNING] Unknown action broadcasted: {action}")


        await self.send(text_data=json.dumps(message))
