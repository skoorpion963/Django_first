import asyncio
from asgiref.sync import sync_to_async
import json
import time 
import websockets
from datetime import datetime


# импорт модели , по совету нейросети 
import os
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'firstproject.settings'
import django
django.setup()
from polls.models import CryptoTransaction , Simbol

# сделки по монете 
class simbol_volue:
    
    # инициализация объекта класса 
    def __init__(self, name,value=None,time = None,
        start = None,count_trades = None):

        self.name = name
        self.value = 0
        self.time = 0
        self.start = True
        self.count_trades = 0

    # пололнение объема
    async def __value_append__(self,value,time):
        if self.start:
            self.time = time
            self.value = value
            self.start = False
            self.count_trades += 1
        else :
            if self.time[4] == time[4]:
                self.value += value
                self.count_trades += 1
            else:
                await self.__print_volue__()
                self.value = value
                self.time = time 
                self.count_trades = 1
                
    # вывод объема за минуту 
    async def __print_volue__(self):

        # print(self.name , " Value :", self.value , "Number of Trades : ",
        #     self.count_trades)

       

        # реализация sync_to_async  
        # кто блин придумал так передавать значения в функцию....       
        await sync_to_async(table_append)(coin_name = self.name,
                                   volume = self.value,
                                   count_trades = self.count_trades)
        
        

        # with ThreadPoolExecutor() as executor:
        #     future = executor.submit(table_append(coin_name = self.name ,
        #             volume= self.value , count_trades = self.count_trades))
        #     result = future.result()
        
     
        

# синхронная функция вставки 
def table_append(coin_name,volume,count_trades):
    simbol = Simbol.objects.get(coin_name=coin_name)
    CryptoTransaction.objects.create(simbol = simbol ,
                    volume= volume,count_trades = count_trades)








# файл с названиями символов
with open('/home/taurus/news_projects/Django_first_project/firstproject/data.json','r') as f:
    data = json.loads(f.read())


# создаю словарь символов и строку для вебсокета 
simbols = []
simbol = {}
url = ''
count = 0
for i in data['simbols']:
    if 'busd' not in i :
        simbol[i] = simbol_volue(i)
        simbols.append(i)
        url = url + i+'@aggTrade/'
        count += 1
url =url[:-1]


# принудительный подсчет объемов за минуту в 1-ую секунду минуты 
async def time_control():
    while True:
        if time.localtime()[5] == 1:
            for i in simbol:
                await simbol[i].__value_append__(0,time.localtime())
        await asyncio.sleep(0.1)

# вывод времени в консоль 
async def time_print():
    while True:
        print(time.strftime('%X'))
        await asyncio.sleep(1)

# подключаюсь к вебсокету и получаю все сделки по запрашиваемым торговы символам 
async def get_trades():
    async with websockets.connect("wss://fstream.binance.com/stream?streams="\
        +url) as websocket:
        
        while True:
            response = await websocket.recv()             
            # достаю информацию о времени и объеме сделки , заполняю словарь 
            data = json.loads(response)
            trans_time = time.localtime(data['data']['T']/1000)
            trans_value = float(data['data']['q'])
            name = data['data']['s'].lower()
            await simbol[name].__value_append__(trans_value,trans_time)


async def main():

    task1 = asyncio.create_task(time_control())
    task2 = asyncio.create_task(get_trades())
    # task3 = asyncio.create_task(time_print())
    
    await task1
    await task2
    # await task3


if __name__ == "__main__":

    asyncio.run(main(),debug=True)
    

    print('done')




