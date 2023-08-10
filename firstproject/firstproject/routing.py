from django.urls import path
from . import consumers
from channels.generic.websocket import AsyncWebsocketConsumer
import json 
import websockets
import time 






websocket_urlpatterns = [
    path('ws/some_path/', consumers.MyConsumer.as_asgi()),
]


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # файл с названиями символов
        with open('data.json','r') as f:
            data = json.loads(f.read())


        # создаю строку для вебсокета 
        url = ''
        count = 0
        for i in data['simbols']:
            if 'busd' not in i :
                if count < 150:
                    url = url + i+'@aggTrade/'
                    count += 1
        url =url[:-1]

        print(url)

        await self.accept()
        async with websockets.connect("wss://fstream.binance.com/stream?streams=" + url) as websocket:
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                trans_time = time.localtime(data['data']['T'] / 1000)
                trans_value = float(data['data']['q'])
                name = data['data']['s'].lower()
                print(data)
                # Здесь вы можете обработать данные и сохранить их в базе данных

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass 