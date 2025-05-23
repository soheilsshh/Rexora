import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.master_id = self.scope['url_route']['kwargs']['master_id']
        self.group_name = f"master_{self.master_id}"


        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"[CONNECTED] Client joined group: {self.group_name}")

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"[DISCONNECTED] Client left group: {self.group_name}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            master_account = data.get('master_account')


            if not master_account:
                await self.send(text_data=json.dumps({
                    'error': 'Missing master_account field.'
                }))
                return


            if master_account != self.master_id:
                await self.send(text_data=json.dumps({
                    'error': 'master_account mismatch. You are connected as: ' + self.master_id
                }))
                return

            if action in ['open_trade', 'modify_trade', 'close_trade', 'open_pending_order']:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'broadcast_message',
                        'message': data
                    }
                )
                print(f"[RECEIVE] Action '{action}' broadcasted in group: {self.group_name}")
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid action type.'
                }))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Unexpected error: {str(e)}'
            }))

    async def broadcast_message(self, event):
        message = event.get('message')
        print(f"[BROADCAST] Sending to group {self.group_name}: {message}")
        await self.send(text_data=json.dumps(message))
