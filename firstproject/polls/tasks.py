import pytz
from .telegram_utils import test , send_info
from celery import shared_task 
from polls.models import CryptoTransaction , BigLimits ,\
    Simbol , BigLimitsEz ,TableView
from datetime import timedelta , datetime
from django.db.models import Prefetch
import signal


simbols_list = ["btcusdt", "ethusdt", "bchusdt", "xrpusdt", "eosusdt", "ltcusdt",
            "trxusdt", "etcusdt", "linkusdt", "xlmusdt", "adausdt", 
            "xmrusdt", "dashusdt", "zecusdt", "xtzusdt", "bnbusdt", 
            "atomusdt", "ontusdt", "iotausdt", "batusdt", "vetusdt", 
            "neousdt", "qtumusdt", "iostusdt", "thetausdt", "algousdt", 
            "zilusdt", "kncusdt", "zrxusdt", "compusdt", "omgusdt", 
            "dogeusdt", "sxpusdt", "kavausdt", "bandusdt", "rlcusdt", 
            "wavesusdt", "mkrusdt", "snxusdt", "dotusdt", "defiusdt", 
            "yfiusdt", "balusdt", "crvusdt", "trbusdt", "runeusdt", 
            "sushiusdt", "srmusdt", "egldusdt", "solusdt", "icxusdt", 
            "storjusdt", "blzusdt", "uniusdt", "avaxusdt", "ftmusdt", 
            "hntusdt", "enjusdt", "flmusdt", "tomousdt", "renusdt", 
            "ksmusdt", "nearusdt", "aaveusdt", "filusdt", "rsrusdt", 
            "lrcusdt", "maticusdt", "oceanusdt", "cvcusdt", "belusdt", 
            "ctkusdt", "axsusdt", "alphausdt", "zenusdt", "sklusdt", 
            "grtusdt", "1inchusdt", "btcbusd", "chzusdt", "sandusdt", 
            "ankrusdt", "btsusdt", "litusdt", "unfiusdt", "reefusdt", 
            "rvnusdt", "sfpusdt", "xemusdt", "btcstusdt", "cotiusdt", 
            "chrusdt", "manausdt", "aliceusdt", "hbarusdt", "oneusdt", 
            "linausdt", "stmxusdt", "dentusdt", "celrusdt", "hotusdt", 
            "mtlusdt", "ognusdt", "nknusdt", "scusdt", "dgbusdt", 
            "1000shibusdt", "bakeusdt", "gtcusdt", "ethbusd", "btcdomusdt", 
            "tlmusdt", "bnbbusd", "adabusd", "xrpbusd", "iotxusdt", 
            "dogebusd", "audiousdt", "rayusdt", "c98usdt", "maskusdt", 
            "atausdt", "solbusd", "fttbusd", "dydxusdt", "1000xecusdt", 
            "galausdt", "celousdt", "arusdt", "klayusdt", "arpausdt", 
            "ctsiusdt", "lptusdt", "ensusdt", "peopleusdt", "antusdt", 
            "roseusdt", "duskusdt", "flowusdt", "imxusdt", "api3usdt", 
            "gmtusdt", "apeusdt", "bnxusdt", "woousdt", "fttusdt", 
            "jasmyusdt", "darusdt", "galusdt", "avaxbusd", "nearbusd", 
            "gmtbusd", "apebusd", "galbusd", "ftmbusd", "dodobusd", 
            "ancbusd", "galabusd", "trxbusd", "1000luncbusd", "luna2busd", 
            "opusdt", "dotbusd", "tlmbusd", "icpbusd", "wavesbusd", 
            "linkbusd", "sandbusd", "ltcbusd", "maticbusd", "cvxbusd", 
            "filbusd", "1000shibbusd", "leverbusd", "etcbusd", "ldobusd", 
            "unibusd", "auctionbusd", "injusdt", "stgusdt", "footballusdt", 
            "spellusdt", "1000luncusdt", "luna2usdt", "ambbusd", "phbbusd", 
            "ldousdt", "cvxusdt", "icpusdt", "aptusdt", "qntusdt", "aptbusd", 
            "bluebirdusdt"]


# создаю слепок таблицы V1 и сохраняю его для удобства пользователей 
@shared_task
def tableV1_update():
    
    current_time = datetime.now()
    timezone = pytz.timezone('Europe/Moscow') 
    current_time =  timezone.localize(current_time) + timedelta(hours=3)

    list_values = []
    row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
        'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}

    # тупая логика , переделать 
    if current_time.second < 3:
        current_time = current_time - timedelta(minutes=1,
                                                 seconds=current_time.second)
        past_minute = current_time + timedelta(seconds=30)
    else:
        past_minute = current_time - timedelta(seconds=current_time.second+1)

    
    symbols = Simbol.objects.prefetch_related(
        Prefetch('cryptotransaction_set',
         queryset=CryptoTransaction.objects.filter(
        timestamp__gte=past_minute, timestamp__lt=current_time)),
        Prefetch('biglimits_set', queryset=BigLimits.objects.all())
            ).all()
    

    for symbol in symbols:
        latest_crypto_transaction = None
        latest_crypto_transactions = symbol.cryptotransaction_set.all()
        if latest_crypto_transactions:
            latest_crypto_transaction = latest_crypto_transactions[0]
       
        biglimits = symbol.biglimits_set.all()
        asks = False
        bids = False
        for limits in biglimits:
            if limits.is_purchase == True:
                bids = limits
            else :
                asks = limits

        row["name"] = symbol.coin_name 
        if latest_crypto_transaction != None:
            row['values']= round(latest_crypto_transaction.volume,2)
            row['count_trades']=latest_crypto_transaction.count_trades
            if bids:
                row['bids'] =  bids.volume[-1]
                row["timeb"] = round((row["bids"]+1)/(row['values']+1),1)
                row['rangeb'] = str(bids.price).rstrip('0')
            if asks:
                row['asks'] = asks.volume[-1]
                row["timea"] = round((row["asks"]+1)/(row['values']+1),1)
                row['rangea'] = str(asks.price).rstrip('0')
        list_values.append(row)
        row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
        'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}       
    # обновляю информацию в базе данных
    try:
        table = TableView.objects.get(name='tableV1')
        table.table = list_values
        table.save()
    except TableView.DoesNotExist:
        TableView.objects.create(name='tableV1', table=list_values)
        print('досадная ошибка V1')
    print('tablev1 done')


# создаю слепок таблицы и сохраняю его для удобства пользователей 
@shared_task
def table_update():

    current_time = datetime.now()
    timezone = pytz.timezone('Europe/Moscow') 
    current_time =  timezone.localize(current_time) + timedelta(hours=3)

    list_values = []
    row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
        'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}

    # тупая логика , переделать 
    if current_time.second < 3:
        current_time = current_time - timedelta(minutes=1,
            seconds=current_time.second)
        past_minute = current_time + timedelta(seconds=30)
    else:
        past_minute = current_time - timedelta(
            seconds=current_time.second+1)

    
    symbols = Simbol.objects.prefetch_related(
        Prefetch('cryptotransaction_set', 
                 queryset=CryptoTransaction.objects.filter(
        timestamp__gte=past_minute, timestamp__lt=current_time)),
    Prefetch('biglimits_set', queryset=BigLimitsEz.objects.all())
        ).all()
    
    
    # print(time.time()-start)
    for symbol in symbols:
        latest_crypto_transaction = None
        latest_crypto_transactions = symbol.cryptotransaction_set.all()
        if latest_crypto_transactions:
            latest_crypto_transaction = latest_crypto_transactions[0]
        # Ваш код обработки
        biglimits = symbol.biglimits_set.all()
        asks = False
        bids = False
        for limits in biglimits:
            if limits.is_purchase == True:
                bids = limits
            else :
                asks = limits

        row["name"] = symbol.coin_name 
        if latest_crypto_transaction != None:
            row['values']= round(latest_crypto_transaction.volume,2)
            row['count_trades']=latest_crypto_transaction.count_trades
            if bids:
                row['bids'] =  bids.volume
                row["timeb"] = round((row["bids"]+1)/(row['values']+1),1)
                row['rangeb'] = bids.price
            if asks:
                row['asks'] = asks.volume
                row["timea"] = round((row["asks"]+1)/(row['values']+1),1)
                row['rangea'] = asks.price
            list_values.append(row)
        row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
        'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}

    # обновляю информацию в базе данных
    try:
        table = TableView.objects.get(name='table')
        table.table = list_values
        table.save()
    except TableView.DoesNotExist:
        TableView.objects.create(name='table', table=list_values)
    print('table done')
   

# загрузка минутных объемов 
@shared_task
def upload_volume():
    import asyncio
    from asgiref.sync import sync_to_async
    import json
    import time 
    import websockets


    connection_true = True
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
                self.list_volumes_received = []
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
            if self.value == 0:
                await self.__connection_check__(0)
            else :
                await self.__connection_check__(1)
        
        # проверка подсчета объемов 
        async def __connection_check__(self,volume):
            if len(self.list_volumes_received) < 154:
                self.list_volumes_received.append(volume)
            else:
                if sum(self.list_volumes_received) == 0:
                    global connection_true 
                    connection_true = False
                    print("переданы пустые объемы , перезапускаю подключение ")
                    send_info("переданы пустые объемы , перезапускаю подключение ")
                    
                else:
                    self.list_volumes_received = []

            
    # создаю словарь символов и строку для вебсокета 
    simbols = []
    simbol = {}
    url = ''
    count = 0
    for i in simbols_list:
        if 'busd' not in i :
            simbol[i] = simbol_volue(i)
            simbols.append(i)
            url = url + i+'@aggTrade/'
            count += 1
    url =url[:-1]


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


    # подключаюсь к вебсокету и получаю все сделки по запрашиваемым торговы символам 
    async def get_trades():

        while True:
            global connection_true
            connection_true = True
            try:
                async with websockets.connect("wss://fstream.binance.com/stream?streams="\
                    +url) as websocket:
                    
                    # если объемы не равны 0 , то соединение работает 
                    while connection_true:
                        response = await websocket.recv()             
                        # достаю информацию о времени и объеме сделки , заполняю словарь 
                        data = json.loads(response)
                        trans_time = time.localtime(data['data']['T']/1000)
                        trans_value = float(data['data']['q'])
                        name = data['data']['s'].lower()
                        await simbol[name].__value_append__(trans_value,trans_time)

            except websockets.exceptions.ConnectionClosedError:
                            # Обработка разрыва соединения
                send_info("Соединение закрыто. Повторная попытка подключения через некоторое время...")
                print("Соединение закрыто. Повторная попытка подключения через некоторое время...")
                await asyncio.sleep(5) 

            except Exception as e:
                # Обработка других исключений
                send_info("Произошла ошибка:", e)


    def handle_interrupt(signum, frame):
        print("Received SIGINT (Ctrl+C)")
        # Здесь вы можете выполнить необходимые действия перед завершением
        # Например, сохранить данные или выполнить завершение задач
        exit(0)  # Выход из программы

    

    async def main():
        # по идее должно выкидывать из бесконечного цикла 
        signal.signal(signal.SIGINT, handle_interrupt)        

        task1 = asyncio.create_task(time_control())
        task2 = asyncio.create_task(get_trades())
        print('upload_volume starting .. ')
        await asyncio.gather(task1, task2)
        print('процесс завершен')

    asyncio.run(main())



# слишком затратно по ресурсам 
# потоковая загрузка стакана 
@shared_task
def upload_deep_book():
    import asyncio 
    import json
    import websockets
    from asgiref.sync import sync_to_async
    import requests
    from queue import Queue



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
        

        # поддержка работы асинхронной петли 
        async def uppdatingTrue(self):
            self.uppdating = True


        # выход из асинхронной петли 
        async def uppdatingFalse(self):
            self.uppdating = False


        # пополнение очереди  
        async def queue_app(self,U,u,pu,asks,bids):
            await self.bufer_event.put([U,u,pu,asks,bids,])
            

        # добавление изменений 
        async def add_changes(self,u,asks,bids):
            self.asks.update(dict(asks))
            self.bids.update(dict(bids))
            self.last_u = u


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
            # print(self.bufer_event.qsize())
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
            while self.uppdating:
                event = await bufer_event.get()
                if event[2] == self.last_u:
                    await self.add_changes(event[1],event[3],event[4])
                else:
                    self.bufer_event = asyncio.Queue()
                    queue_snip.put(self.name)
                    print('поток прерван')
                    break
            if self.uppdating is False:
                self.bufer_event = asyncio.Queue()


    # получение снимка стакана 
    def get_book_snap(simbol):
        return requests.get(
            f'https://fapi.binance.com/fapi/v1/depth?symbol={simbol.upper()}&limit=1000'
            ).json()

    # получение снимка стакана , и запуск корутины по обработке потока 
    async def get_order_book_snapshot(queue_snip,simbols):
        loop2 = asyncio.get_event_loop()
        while True:
            if queue_snip.empty() is False:
                simbol = queue_snip.get()
                order_book = await sync_to_async(get_book_snap)(simbol)
                try:
                    bids = order_book['bids']
                    asks = order_book['asks']
                    lastUpdateId = order_book['lastUpdateId']
                    print('получил снимок , отправляю')
                    
                    asyncio.run_coroutine_threadsafe(simbols[simbol].
                        get_snap(asks,bids,lastUpdateId), loop2)
                    print('отправил снимок ')
                
                except KeyError :
                    print(simbol,'  msg: ',order_book['msg'])
            else:
                await asyncio.sleep(0.1)

        
    # подписка и отписка на потоки указанные в очередях
    async def subscribe_to_streams(add,dell,simbols):
        try:
            url = f"wss://fstream.binance.com/ws/"
            async with websockets.connect(url) as websocket:
                while True:
                    # подписка
                    while add.empty() is False:
                        simbols_name  = add.get()
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": [simbols_name +'@depth'],
                            "id": 1
                        }
                        await websocket.send(json.dumps(subscribe_request))
                        simbols[simbols_name].uppdatingTrue()

                    # отписка  
                    while dell.empty() is False:
                        simbols_name  = dell.get()
                        subscribe_request = {
                            "method": "UNSUBSCRIBE",
                            "params": [simbols_name+'@depth'],
                            "id": 1
                        }
                        await websocket.send(json.dumps(subscribe_request))
                        simbols[simbols_name].uppdatingFalse()

                    # прослушивание сокета и отправка сообщений по буферам символов 
                    response = await websocket.recv()
                    data = json.loads(response)
                    order_book = data['data']
                    await simbols[order_book['s'].lower()].queue_app(
                        U = order_book['U'],u = order_book['u'],pu = order_book['pu'],
                        bids = order_book['b'],asks = order_book['a']
                    )

        except websockets.exceptions.ConnectionClosedError:
                        # Обработка разрыва соединения
            send_info("Соединение закрыто. Повторная попытка подключения через некоторое время...")
            await asyncio.sleep(5) 

        except Exception as e:
            # Обработка других исключений
            send_info("Произошла ошибка:", e)


    
    # получаю список имен всех искомых объектов
    def get_names_list():
        return list(BigLimits.objects.values_list(
            'simbol__coin_name', flat=True))


    # анализирую большие заявки , при появлении новых добавляю их в очередь на добавление 
    # если текущие заявки разъедены , добавяю в очередь на отписку 
    async def chek_limits(add, dell, queue_snip):
        curr_lims = []
        names_list = await sync_to_async(get_names_list)()
        curr_lims = names_list
        for i in names_list:
            add.put(i)
            queue_snip.put(i)
        while True:
            names_list = await sync_to_async(get_names_list)()
            if names_list != curr_lims:
                del_list = curr_lims - names_list
                add_list = names_list - curr_lims
                if del_list:
                    for i in del_list:
                        await dell.put(i)
                if add_list:
                    for i in add_list:
                        await add.put(i)
                        queue_snip.put(i)
            else:
                asyncio.sleep(0.1)


    async def main():
        while True:
            try:
                queue_add = Queue()
                queue_dell = Queue()
                queue_snip = Queue()
                # создание словаря с объектами класса 
                simbols = {}
                for i in simbols_list:
                    simbols[i] = SimbolsV2(i)

                task1 = asyncio.create_task(subscribe_to_streams(
                    queue_add, queue_dell, simbols))
                
                task2 = asyncio.create_task(get_order_book_snapshot(
                    queue_snip, simbols))
                
                task3 = asyncio.create_task(chek_limits(
                    queue_add, queue_dell, queue_snip))
                
                await asyncio.gather(task1, task2, task3)
            
            except Exception as ex:
                send_info("перезапуск потоковой загрузки стакана в \
                           следствии ошибки : ", ex)
                await asyncio.sleep(1)  


    if __name__ == "__main__":
        asyncio.run(main(),debug=True)


@shared_task
def density_search():
    import requests
    from django.utils import timezone
    from requests.exceptions import ConnectionError
    from polls.models import CryptoTransaction , Simbol ,BigLimits ,BigLimitsEz






    def add_log(info):
        with open('firstproject/log.txt', 'a') as f:
            f.writelines(info)

    #  удаление съеденных заявок 
    def cleaning_big_limits(simbol, my_dict, is_purchase):
        simbol = Simbol.objects.get(coin_name=simbol)
        bigLimits = BigLimits.objects.filter(simbol=simbol, is_purchase=is_purchase)
        
        if bigLimits:
            for bigLimit in bigLimits:
                key = bigLimit.price
                # в дикте значения с нулями на конце а из объекте биглимитс без конца на нуле , понять почему так происходит 
                if float(key) not in my_dict or bigLimit.volume[0]*0.4 > \
                    float(my_dict[float(key)]):
                    print(f"удалена заявка {simbol.coin_name} : {is_purchase} ")
                    bigLimit.delete()
                    
    

    # проверка большой заявки , существование оной 
    def sheck_big_limits(simbol,volume,price,difference,is_purchase,my_dict):
        simbol_name = Simbol.objects.get(coin_name=simbol)
        bigLimits = BigLimits.objects.filter(simbol=simbol_name,is_purchase = is_purchase, price = price)
        
        my_dict1 = my_dict
        if len(bigLimits) == 1:
            apdate_big_limits(bigLimits,volume,difference)
        elif len(bigLimits) == 0:
            # цена уже тут без нулей на конце ...
            save_big_limits(simbol= simbol, price = price, volume = volume, is_purchase =is_purchase, 
                        difference = difference )
            
            print(f'Крупная заявка {simbol} количество монет: {volume} цена:{price} расстояние:{difference}')
            
        else:
            print(len(bigLimits))
            
    # сохраняю самую большую заявку 
    def save_ez_big_limits(simbol,volume,price,range,is_purchase):
        
        simbol = Simbol.objects.get(coin_name=simbol)
        BigLimitsEz.objects.filter(simbol = simbol,is_purchase =is_purchase).delete()
        BigLimitsEz.objects.create(simbol = simbol, 
                                volume = volume ,price = price ,range=range,is_purchase = is_purchase)


    # сохранение большой заявки 
    def save_big_limits(simbol,volume,price,difference,is_purchase):
        print(simbol,volume,price,is_purchase)
        simbol = Simbol.objects.get(coin_name=simbol)
        BigLimits.objects.create(simbol=simbol,
                            price = price, volume = [volume],
                            is_purchase = is_purchase, 
                            changes = [difference]  ,
                            timestamp  = [timezone.now()],       
                                )
        

    # обновляю значения 
    def apdate_big_limits(big_limits, volume,difference,):
        big_limits[0].volume.append(volume)
        big_limits[0].changes.append(difference)
        big_limits[0].timestamp.append(timezone.now())
        big_limits[0].save()
        print(f'Изменение крупной заявки {big_limits[0].simbol.coin_name} , id = {big_limits[0].id}')


    # получаем имена всех монет , flat=True что бы получить список имен а не кортежей
    def get_simbol_names():
        simbols =  list(Simbol.objects.values_list('coin_name', flat=True))
        
        return simbols
    

    # получаем список последних 60 объемов искомой монеты 
    def get_simbol_volume(simbol):
        simbol = Simbol.objects.get(coin_name=simbol)
        simbol_volues = list(CryptoTransaction.objects.filter(simbol = simbol,).\
            order_by('-timestamp')[:60].values_list('volume', flat=True))
        return simbol_volues


    # получаю слепок стакана использую реквесты что бы не перегружать код, вебсокетом 
    # увеличивается сложность , а мы ищем редкие продолжительные явления 
    def get_order_book(simbol):
        while True:
            try:
                return requests.get(f'https://fapi.binance.com/fapi/v1/depth?symbol={simbol.upper()}&limit=1000').json()
            except ConnectionError as e:
                print(f'Ошибка соедиения: {e}. Повторная попытка')


    # возвращает максимальный объем 
    def max_volume(b_depth):
        answer =[1,1]
        for i,j in b_depth:
            if float(i)*float(j) > float(answer[0])*float(answer[1]):
                answer = [i,j]
        return answer
        

    # добавляю третью колонку для нахождения суммы всех объемов на этом уровне 
    def add_cumulative_sum(list):
        result = []
        sum_ = 0
        for item in list:
            sum_ += float(item[1])*float(item[0])
            result.append([float(item[0]), float(item[1]), sum_])
        return result


    # поиск плотности 
    def density_search_1(simbol_volume,simbol_book_depth,simbol):
        # пробегаю по списку плотностей и сохраняю сумму
        #  всех объемов до этой плотности в новой колонке рядом 
        bids = add_cumulative_sum(simbol_book_depth['bids'])
        asks = add_cumulative_sum(simbol_book_depth['asks'])

        # нахожу максимальные плотности и сохраняю их    
        mbids  = max_volume(simbol_book_depth['bids'])
        masks  = max_volume(simbol_book_depth['asks'])
        rangeB = round(float(simbol_book_depth['bids'][0][0])/float(mbids[0])*100-100,2)
        rangeA = round(float(masks[0])/float(simbol_book_depth['asks'][0][0])*100-100,2)
        save_ez_big_limits(simbol,mbids[1],mbids[0],rangeB,False)
        save_ez_big_limits(simbol,masks[1],masks[0],rangeA,True)

        # работает как попало 
        bids_dict =  {float(x[0]): float(x[1]) for x in simbol_book_depth['bids']}
        asks_dict =  {float(x[0]): float(x[1]) for x in simbol_book_depth['asks']}
        cleaning_big_limits(simbol,bids_dict,False)
        cleaning_big_limits(simbol,asks_dict,True)

        bids_ansver = []
        asks_ansver = []

        # ищу заявки которые больше суммы предведущих заявок и больше объема торгов за минуту 
        # и после которых нет других крупных заявок 
        # одинокие крупные заявки 
        for id, item  in enumerate(asks):
            if id < 100:
                if id != 0:
                    if item[1]*item[0]/2 > item[2]-item[1]*item[0] \
                        and item[1]>simbol_volume*2 \
                        and asks[id+10][2] - item[2] < item[0]*item[1]/2:
                            asks_ansver = item
                else:
                    if item[1]>simbol_volume*2 \
                        and asks[id+10][2] - item[2] < item[0]*item[1]/2:
                            asks_ansver = item

        for id, item in enumerate(bids):
            if id < 100:
                if id != 0:
                    if item[1]*item[0]/2 > item[2]-item[1]*item[0] \
                        and item[1]>simbol_volume*2 \
                        and bids[id+10][2] - item[2] < item[0]*item[1]/2:
                            bids_ansver = item
                else:
                    if item[1]>simbol_volume*2 \
                        and bids[id+10][2] - item[2] < item[0]*item[1]/2:
                            bids_ansver = item
                        
        
        if asks_ansver != []:
            # переменная отвечающая за дальность заявки от текущей цены 
            range = float(asks_ansver[0])/float(simbol_book_depth['asks'][0][0])*100-100
            # насколько заявка больше предложения до нее
            difference = float(asks_ansver[1])/(float(asks_ansver[2])-float(asks_ansver[1]))*100-100
            if range > 0.1 and range < 200:
                sheck_big_limits(simbol=simbol,volume=asks_ansver[1],price=asks_ansver[0],difference=range,is_purchase=True,my_dict =asks_dict)
                
                print(f"Крупная заявка ,на покупку {simbol} :" , asks_ansver[0],asks_ansver[1], " Дальность : ","%.2f" % range,'%' )
                print("Привышение суммы объема в стакане до заявки на  ",difference ,' %')


        if bids_ansver != []:
            range = float(simbol_book_depth['bids'][0][0])/float(bids_ansver[0])*100-100
            difference = float(bids_ansver[1])/(float(bids_ansver[2])-float(bids_ansver[1]))*100-100
            if range > 0.1 and range < 200:
                sheck_big_limits(simbol=simbol,volume=bids_ansver[1],price=bids_ansver[0],difference=range,is_purchase=False, my_dict =bids_dict)
                
                print(f"Крупная заявка ,на продажу {simbol} :" , bids_ansver[0],bids_ansver[1], " Дальность : ","%.2f" % range,'%' )
                print("Привышение суммы объема в стакане до заявки на  ",difference ,' %')

    def handle_interrupt(signum, frame):
        print("Received SIGINT (Ctrl+C)")
        # Здесь вы можете выполнить необходимые действия перед завершением
        # Например, сохранить данные или выполнить завершение задач
        exit(0)  # Выход из программы

    
        
    def main():
        simbols  = get_simbol_names()
        print(len(simbols))
        signal.signal(signal.SIGINT, handle_interrupt)
        while True:
            
            for simbol in simbols:
                
                order_book = get_order_book(simbol=simbol)
                simbol_volues = get_simbol_volume(simbol=simbol)
                if order_book['bids'] != [] and order_book['asks'] !=0 : 
                    if len(order_book)!= 2 and simbol_volues !=0:
                        density_search_1(
                            simbol_volume = sum(simbol_volues)/len(simbol_volues),
                            simbol_book_depth = order_book,
                            simbol = simbol,
                        )
                else:
                    print(simbol , 'в ответе сервера пустой стакан')


    
    main()  




# запуск загрузки минутных объемов 
upload_volume.delay()

# попробовать запуск в синхронном режиме
density_search.delay()

