import asyncio
from asgiref.sync import sync_to_async
import json
import time 
import websockets
from celery import Celery
from polls import telegram_utils
from polls.models import CryptoTransaction , Simbol



# # импорт модели , по совету нейросети 
# import os
# from django.conf import settings
# os.environ['DJANGO_SETTINGS_MODULE'] = 'firstproject.settings'
# import django
# django.setup()



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

        # реализация sync_to_async  
        # кто блин придумал так передавать значения в функцию....       
        await sync_to_async(table_append)(coin_name = self.name,
                                   volume = self.value,
                                   count_trades = self.count_trades)
        
        

# файл с названиями символов
with open('firstproject/polls/upload_volume/data.json','r') as f:
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

def add_log(info):
    with open('firstproject/log.txt', 'a') as f:
        f.write(info,'\n')


# синхронная функция вставки в таблицу
def table_append(coin_name,volume,count_trades):
    simbol = Simbol.objects.get(coin_name=coin_name)
    CryptoTransaction.objects.create(simbol = simbol ,
                    volume= volume,count_trades = count_trades)




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
    while True:
        try:
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

                    if 'ping' in data:
                        ping = data['ping']
                        await websocket.send(json.dumps({"pong": ping}))
                        telegram_utils.send_info("отправил понг")

        except websockets.exceptions.ConnectionClosedError:
                        # Обработка разрыва соединения
            telegram_utils.send_info("Соединение закрыто. Повторная попытка подключения через некоторое время...")
            print("Соединение закрыто. Повторная попытка подключения через некоторое время...")
            await asyncio.sleep(5) 

        except Exception as e:
            # Обработка других исключений
            telegram_utils("Произошла ошибка:", e)
            print("Произошла ошибка:", e)



# не работает 
# проверка стакана на интересные плотности 
# async def sheck_order_book():
#    await sync_to_async(density_search.main)()


async def main():

    task1 = asyncio.create_task(time_control())
    task2 = asyncio.create_task(get_trades())
    # thread = threading.Thread(target=density_search.main)
    # thread.start()
    # task3 = asyncio.create_task(sheck_order_book())
    
    
    await task1
    await task2
    # await task3

    asyncio.run(main(),debug=True)
    

if __name__ == '__main__':
    asyncio.run(main(), debug=True)





