import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import django
django.setup()
from .models import ChatRoom, Chat
class ChatRoomConsumer(AsyncWebsocketConsumer):
     async def connect(self):
          self.room_name = self.scope['url_route']['kwargs']['room_name']
          self.room_group_name = 'chat_%s' % self.room_name

          await self.channel_layer.group_add(
               self.room_group_name,
               self.channel_name
          )

          await self.accept()

     async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
              self.room_group_name,
              self.channel_name
         )
     
     async def receive(self,text_data):
          text_data_json = json.loads(text_data)
          message = text_data_json['message']
          username = text_data_json['username']
          self.user_id = self.scope['user'].id

          #Find room object
          room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

          chat = Chat(
               content = message,
               user = self.scope['user'],
               room=room
          )

          await database_sync_to_async(chat.save)()
          
          await self.channel_layer.group_send(
               self.room_group_name,
               {
                    'type':'chatroom_message',
                    'message' : message,
                    'username': username,
                    'user_id':self.user_id
               }
          )
     async def chatroom_message(self,event):
          message = event['message']
          username = event['username']
          user_id = event['user_id']

          await self.send(text_data=json.dumps({
               'message': message,
               'username': username,
               'user_id':user_id
          }))
