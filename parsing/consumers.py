import json, os, importlib, inspect
from channels.generic.websocket import WebsocketConsumer
from .views import import_dict
# from django.utils import timezone
# from datetime import timedelta
# import time

class ParsingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
       
    # Receive message from WebSocket
    def receive(self, text_data):
        json_get = json.loads(text_data)
        if 'file' in json_get:
            file = json_get['file']
            fid = json_get['id']
            for key in import_dict:
                for value in import_dict[key]:
                    if value.lower() in file.lower():
                        parser = os.path.join(os.getcwd(), 'parsing', 'parsers', key + '.py')
                        spec = importlib.util.spec_from_file_location(key + '.' + 'py', parser)
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                        result = getattr(foo, key)(file, key)
                        for res in result:
                            if isinstance(res, int):
                                self.send(text_data=json.dumps({fid: res}))
                            else:
                                self.send(text_data=json.dumps({fid: 'error'}))
            self.send(text_data=json.dumps({fid: 'parsed'}))
        else:
            self.send(text_data=json.dumps({'Error', 'No file in request'}))
            self.close()
        # self.close()

    # def disconnect(self, event):
    #     self.close()

# import json
# from channels.generic.websocket import WebsocketConsumer
# from django.utils import timezone
# from datetime import timedelta
# import time

# class ParsingConsumer(WebsocketConsumer):
#     def connect(self):
#         # play_id = self.scope['url_route']['kwargs']['play_id']
#         # print('ok')
#         self.accept()
#         # print('ok')
#         # print(self.scope)
#         start = timezone.now()
        
#         for i in range(1, 10):
#             print(i)
#             now = timezone.now()
#             apm = i
#             elapsed = (now - start).seconds

#             self.send(text_data=json.dumps({
#                 'apm': apm,
#                 'ellapsed': elapsed
#                 }))

#             time.sleep(0.5)
#         # break
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(text_data)
#         # message = text_data_json['message']

#         # # Send message to room group
#         # async_to_sync(self.channel_layer.group_send)(
#         #     self.room_group_name,
#         #     {
#         #         'type': 'chat_message',
#         #         'message': message
#         #     }
#         # )
