coins = ['btcusdt', 'ethusdt', 'bchusdt', 'xrpusdt', 'eosusdt', 'ltcusdt', 'trxusdt', 'etcusdt', 'linkusdt', 'xlmusdt', 'adausdt', 'xmrusdt', 'dashusdt', 'zecusdt', 'xtzusdt', 'atomusdt', 'ontusdt', 'iotausdt', 'batusdt', 'vetusdt', 'neousdt', 'qtumusdt', 'iostusdt', 'thetausdt', 'algousdt', 'zilusdt', 'kncusdt', 'zrxusdt', 'compusdt', 'omgusdt', 'dogeusdt', 'sxpusdt', 'kavausdt', 'bandusdt', 'rlcusdt', 'wavesusdt', 'mkrusdt', 'snxusdt', 'dotusdt', 'defiusdt', 'yfiusdt', 'balusdt', 'crvusdt', 'runeusdt', 'sushiusdt', 'srmusdt', 'egldusdt', 'solusdt', 'icxusdt', 'storjusdt', 'blzusdt', 'uniusdt', 'avaxusdt', 'ftmusdt', 'hntusdt', 'enjusdt', 'flmusdt', 'tomousdt', 'renusdt', 'ksmusdt', 'nearusdt', 'aaveusdt', 'filusdt', 'rsrusdt', 'lrcusdt', 'maticusdt', 'oceanusdt', 'cvcusdt', 'belusdt', 'ctkusdt', 'axsusdt', 'alphausdt', 'zenusdt', 'sklusdt', 'grtusdt', '1inchusdt', 'chzusdt', 'sandusdt', 'ankrusdt', 'btsusdt', 'litusdt', 'unfiusdt', 'reefusdt', 'rvnusdt', 'sfpusdt', 'xemusdt', 'btcstusdt', 'cotiusdt', 'chrusdt', 'manausdt', 'aliceusdt', 'hbarusdt', 'oneusdt', 'linausdt', 'stmxusdt', 'dentusdt', 'celrusdt', 'hotusdt', 'mtlusdt', 'ognusdt', 'nknusdt', 'scusdt', 'bakeusdt', 'gtcusdt', 'btcdomusdt', 'tlmusdt', 'iotxusdt', 'audiousdt', 'rayusdt', 'c98usdt', 'maskusdt', 'atausdt', 'dydxusdt', '1000xecusdt', 'galausdt', 'celousdt', 'arusdt', 'klayusdt', 'arpausdt', 'ctsiusdt', 'lptusdt', 'ensusdt', 'peopleusdt', 'antusdt', 'roseusdt', 'duskusdt', 'flowusdt', 'imxusdt', 'api3usdt', 'gmtusdt', 'apeusdt', 'bnxusdt', 'woousdt', 'fttusdt', 'jasmyusdt', 'darusdt', 'galusdt', 'opusdt', 'injusdt', 'stgusdt', 'footballusdt', 'spellusdt', '1000luncusdt', 'luna2usdt', 'ldousdt', 'cvxusdt', 'icpusdt', 'aptusdt', 'qntusdt', 'bluebirdusdt']


import asyncio 
import json
import websockets
from asgiref.sync import sync_to_async
import requests
from queue import Queue


update_count = 0

class SimbolsV2:


    # инициализация 
    def __init__(self,name):
        self.name = name
        self.bids = {}
        self.asks = {}
        self.lastUpdateId = None
        self.last_u = None
        self.stream = False
        self.bufer_event = asyncio.Queue()
        self.uppdating = False
        self.first_event_work = False
    

    # тест 
    # пополнение очереди  
    async def queue_app(self,U,u,pu,asks,bids):
         await self.bufer_event.put([U,u,pu,asks,bids,])
        

    # добавление изменений 
    async def add_changes(self,u,asks,bids):
        self.asks.update(dict(asks))
        self.bids.update(dict(bids))
        self.last_u = u
        # print(self.name , ' добавил изменения')


    # получение снимка стакана 
    async def get_snap(self,asks,bids,lastUpdateId):
        self.asks = dict(asks)
        self.bids = dict(bids)
        self.lastUpdateId = lastUpdateId
        await self.first_event(self.bufer_event)
        # в методе get_order_book_snapshot
        await self.add_recent_changes(self.bufer_event)


    # поиск первого события из буфера 
    async def first_event(self,bufer_event):
        print(self.bufer_event.qsize())
        try:
            while True:
                event = await bufer_event.get()
                if event[0] < self.lastUpdateId and event[1] >= self.lastUpdateId:
                    await self.add_changes(event[1],event[3],event[4])
                    break
        except Exception as ex:
            print('ошибка', ex)


    # обработка последующих сообщений из буфура 
    async def add_recent_changes(self,bufer_event):
        print('ищу последующие события')
        global queue_snip
        while True:
            event = await bufer_event.get()
            if event[2] == self.last_u:
                await self.add_changes(event[1],event[3],event[4])
            else:
                self.bufer_event = asyncio.Queue()
                queue_snip.put(self.name)
                print('поток прерван')
                break


def get_book_snap(simbol):
    return requests.get(
        f'https://fapi.binance.com/fapi/v1/depth?symbol={simbol.upper()}&limit=1000'
        ).json()


async def get_order_book_snapshot(queue_snip,simbols):
    loop2 = asyncio.get_event_loop()
    while True:
        if queue_snip.empty() is False:
            simbol = queue_snip.get()
            print(simbol)
            order_book = await sync_to_async(get_book_snap)(simbol)
            try:
                bids = order_book['bids']
                asks = order_book['asks']
                lastUpdateId = order_book['lastUpdateId']
                print('получил снимок , отправляю')
                
                asyncio.run_coroutine_threadsafe(simbols[simbol].get_snap(asks,bids,lastUpdateId), loop2)
                # await simbols[simbol].get_snap(asks,bids,lastUpdateId)
                print('отправил снимок ')
             
            except KeyError :
                print(simbol,'  msg: ',order_book['msg'])
        else:
            await asyncio.sleep(0.1)


async def subscribe_to_order_book_updates(url, simbols):
    url = f"wss://fstream.binance.com/stream?streams={url}"

    async with websockets.connect(url) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            order_book = data['data']
            await simbols[order_book['s'].lower()].queue_app(
                U = order_book['U'],u = order_book['u'],pu = order_book['pu'],
                bids = order_book['b'],asks = order_book['a']
            )
      

async def subscribe_to_streams(coins):
    coins_current  = coins 
    
    url = f"wss://fstream.binance.com/ws/"
    async with websockets.connect(url) as websocket:
        for stream in streams:
            subscribe_request = {
                "method": "SUBSCRIBE",
                "params": [stream],
                "id": 1
            }
            await websocket.send(json.dumps(subscribe_request))

        while True:
            response = await websocket.recv()






async def chek_limits():
    

    pass

# async def main():
#     # создание словаря с объектами класса 
#     queue_snip = Queue()
#     url = ''
#     simbols = {}
#     count = 0
#     for i in coins:
#         simbols[i] = SimbolsV2(i)
#         queue_snip.put(i)
#         url += i + '@depth/'
#         count +=1 
#     url =url[:-1]


#     task1 = asyncio.create_task(subscribe_to_order_book_updates(url,simbols))
#     await asyncio.sleep(2)
#     task2 = asyncio.create_task(get_order_book_snapshot(queue_snip,simbols))
#     print('upload_volume starting .. ')
#     await asyncio.gather(task1, task2)
  
    
# if __name__ == "__main__":
#     asyncio.run(main(),debug=True)


async def main():
    
    streams_to_subscribe = ["btcusdt@aggTrade", "btcusdt@depth"]
    task1 = asyncio.create_task(subscribe_to_streams(url,streams_to_subscribe))
    await asyncio.gather(task1)


if __name__ == "__main__":
    asyncio.run(main(),debug=True)
