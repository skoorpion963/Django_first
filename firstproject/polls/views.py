
from django.http import HttpResponse
from polls.models import CryptoTransaction , BigLimits , Simbol , BigLimitsEz , TableView
from django.shortcuts import render , redirect
from rest_framework import generics
from .serializers import *
from datetime import datetime , timedelta
from rest_framework.response import Response
from rest_framework.views import View
from django.db.models import Sum





def home(request):
    return render(request, 'polls/home.html')

def api(request):
    return render(request, 'polls/api.html')



def tableV1(request):
    headers = ['Название','Объем/мин','fshort','Время','Цена','flong','Время','Цена',]
    list = TableView.objects.get(name='tableV1').table
    list1 = list[:50]
    list2 = list[50:100]
    list3 = list[100:]
    return render(request, 'polls/tablev1.html', {'title': "Главная страница ", 
                    'list1':list1,'list2':list2,'list3':list3 , 'headers': headers })

def table(request):
    headers = ['Название','Объем/мин','fshort','Время','Цена','flong','Время','Цена',]
    list = TableView.objects.get(name='table').table
    list1 = list[:50]
    list2 = list[50:100]
    list3 = list[100:]
    return render(request, 'polls/table.html', {'title': "Главная страница ", 
                    'list1':list1,'list2':list2,'list3':list3 , 'headers': headers })


def table__(request):
    simbols_list = ["btcusdt", "ethusdt", "bchusdt", "xrpusdt", "eosusdt",
                 "ltcusdt", "trxusdt", "etcusdt", "linkusdt", "xlmusdt",
                "adausdt", "xmrusdt", "dashusdt", "zecusdt", "xtzusdt", 
                "atomusdt", "ontusdt", "iotausdt", "batusdt", "vetusdt", 
                "neousdt", "qtumusdt", "iostusdt", "thetausdt", "algousdt", 
                "zilusdt", "kncusdt", "zrxusdt", "compusdt", "omgusdt", 
                "dogeusdt", "sxpusdt", "kavausdt", "bandusdt", "rlcusdt", 
                "wavesusdt", "mkrusdt", "snxusdt", "dotusdt", "defiusdt", 
                "yfiusdt", "balusdt", "crvusdt", "runeusdt", "sushiusdt", 
                "srmusdt", "egldusdt", "solusdt", "icxusdt", "storjusdt", 
                "blzusdt", "uniusdt", "avaxusdt", "ftmusdt", "hntusdt", 
                "enjusdt", "flmusdt", "tomousdt", "renusdt", "ksmusdt", 
                "nearusdt", "aaveusdt", "filusdt", "rsrusdt", "lrcusdt", 
                "maticusdt", "oceanusdt", "cvcusdt", "belusdt", "ctkusdt", 
                "axsusdt", "alphausdt", "zenusdt", "sklusdt", "grtusdt", 
                "1inchusdt", "chzusdt", "sandusdt", "ankrusdt", "btsusdt", 
                "litusdt", "unfiusdt", "reefusdt", "rvnusdt", "sfpusdt", 
                "xemusdt", "btcstusdt", "cotiusdt", "chrusdt", "manausdt", 
                "aliceusdt", "hbarusdt", "oneusdt", "linausdt", "stmxusdt", 
                "dentusdt", "celrusdt", "hotusdt", "mtlusdt", "ognusdt", 
                "nknusdt", "scusdt", "bakeusdt", "gtcusdt", "btcdomusdt", 
                "tlmusdt", "iotxusdt", "audiousdt", "rayusdt", "c98usdt",
                "maskusdt", "atausdt", "dydxusdt", "1000xecusdt", "galausdt", 
                "celousdt", "arusdt", "klayusdt", "arpausdt", "ctsiusdt", 
                "lptusdt", "ensusdt", "peopleusdt", "antusdt", "roseusdt", 
                "duskusdt", "flowusdt", "imxusdt", "api3usdt", "gmtusdt", 
                "apeusdt", "bnxusdt", "woousdt", "fttusdt", "jasmyusdt", 
                "darusdt", "galusdt", "opusdt", "injusdt", "stgusdt", 
                "footballusdt", "spellusdt", "1000luncusdt", "luna2usdt", 
                "ldousdt", "cvxusdt", "icpusdt", "aptusdt", "qntusdt", 
                "bluebirdusdt", ]
    
    # headers = ['Название','Объем/мин','fshort','Время','Растояние','flong','Время','Растояние','Сделок']
    headers = ['Название','Объем/мин','fshort','Вреямя','Растояние','flong','Время','Растояние',]
    list_values = []
    row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
           'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}

    for simbol in simbols_list:
        last_values = CryptoTransaction.objects.filter(simbol__coin_name=simbol).order_by('-id').first()
       
        bids_limits = BigLimitsEz.objects.filter(simbol__coin_name = simbol,is_purchase = False)
        if bids_limits:
            if float(last_values.volume)*2 < float(bids_limits[0].volume):
                row['bids'] = bids_limits[0].volume
                row["timeb"] = round((row["bids"]+1)/(last_values.volume+1),1)

                row['rangeb'] = str(bids_limits[0].range) + " %"


        asks_limits = BigLimitsEz.objects.filter(simbol__coin_name = simbol,is_purchase = True)
        if asks_limits:
            if float(last_values.volume)*2 < float(asks_limits[0].volume):
                row['asks'] = asks_limits[0].volume
                row["timea"] = round((row["asks"]+1)/(last_values.volume+1),1)
                row['rangea'] = str(asks_limits[0].range) + " %"
        
        row["name"] = (last_values.simbol.coin_name).upper()
        row['values']=(round(last_values.volume,2))
        row['count_trades']=(last_values.count_trades)
    
        list_values.append(row)
        row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
           'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}
        # row = {'name': '', 'values':'','bids':' - ','asks':' - ','count_trades':''}
        # row = {'name': '', 'values':'','bids':' - ','asks':' - ',}

    

    list1 = list_values[:50]
    list2 = list_values[50:100]
    list3 = list_values[100:]

    context = {'list1':list1,'list2':list2,'list3':list3}


    return render(request, 'polls/table.html', {'title': "Главная страница ", 
                    'list1':list1,'list2':list2,'list3':list3 , 'headers': headers })
    

def tableV1__(request):

    import time 
    start = time.time()

    simbols_list = ["btcusdt", "ethusdt", "bchusdt", "xrpusdt", "eosusdt",
                 "ltcusdt", "trxusdt", "etcusdt", "linkusdt", "xlmusdt",
                "adausdt", "xmrusdt", "dashusdt", "zecusdt", "xtzusdt", 
                "atomusdt", "ontusdt", "iotausdt", "batusdt", "vetusdt", 
                "neousdt", "qtumusdt", "iostusdt", "thetausdt", "algousdt", 
                "zilusdt", "kncusdt", "zrxusdt", "compusdt", "omgusdt", 
                "dogeusdt", "sxpusdt", "kavausdt", "bandusdt", "rlcusdt", 
                "wavesusdt", "mkrusdt", "snxusdt", "dotusdt", "defiusdt", 
                "yfiusdt", "balusdt", "crvusdt", "runeusdt", "sushiusdt", 
                "srmusdt", "egldusdt", "solusdt", "icxusdt", "storjusdt", 
                "blzusdt", "uniusdt", "avaxusdt", "ftmusdt", "hntusdt", 
                "enjusdt", "flmusdt", "tomousdt", "renusdt", "ksmusdt", 
                "nearusdt", "aaveusdt", "filusdt", "rsrusdt", "lrcusdt", 
                "maticusdt", "oceanusdt", "cvcusdt", "belusdt", "ctkusdt", 
                "axsusdt", "alphausdt", "zenusdt", "sklusdt", "grtusdt", 
                "1inchusdt", "chzusdt", "sandusdt", "ankrusdt", "btsusdt", 
                "litusdt", "unfiusdt", "reefusdt", "rvnusdt", "sfpusdt", 
                "xemusdt", "btcstusdt", "cotiusdt", "chrusdt", "manausdt", 
                "aliceusdt", "hbarusdt", "oneusdt", "linausdt", "stmxusdt", 
                "dentusdt", "celrusdt", "hotusdt", "mtlusdt", "ognusdt", 
                "nknusdt", "scusdt", "bakeusdt", "gtcusdt", "btcdomusdt", 
                "tlmusdt", "iotxusdt", "audiousdt", "rayusdt", "c98usdt",
                "maskusdt", "atausdt", "dydxusdt", "1000xecusdt", "galausdt", 
                "celousdt", "arusdt", "klayusdt", "arpausdt", "ctsiusdt", 
                "lptusdt", "ensusdt", "peopleusdt", "antusdt", "roseusdt", 
                "duskusdt", "flowusdt", "imxusdt", "api3usdt", "gmtusdt", 
                "apeusdt", "bnxusdt", "woousdt", "fttusdt", "jasmyusdt", 
                "darusdt", "galusdt", "opusdt", "injusdt", "stgusdt", 
                "footballusdt", "spellusdt", "1000luncusdt", "luna2usdt", 
                "ldousdt", "cvxusdt", "icpusdt", "aptusdt", "qntusdt", 
                "bluebirdusdt", ]
    
    # headers = ['Название','Объем/мин','fshort','Вреямя','Растояние','flong','Время','Растояние','Сделок']
    headers = ['Название','Объем/мин','fshort','Вреямя','Растояние','flong','Время','Растояние',]

    list_values = []
    row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
           'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}
    # simbols_list = CryptoTransaction.objects.filter(simbol__coin_name__in=simbols_list)

    for simbol in simbols_list:
        last_values = CryptoTransaction.objects.filter(simbol__coin_name=simbol).order_by('-id').first()
       
        bids_limits = BigLimits.objects.filter(simbol__coin_name = simbol,is_purchase = False)
        if bids_limits:
            row['bids'] = bids_limits.last().volume[-1] 
            row["timeb"] = round((row["bids"]+1)/(last_values.volume+1),1)
            row['rangeb'] = round(bids_limits.last().changes[-1],2)

        asks_limits = BigLimits.objects.filter(simbol__coin_name = simbol,is_purchase = True)
        if asks_limits:
            row['asks'] = asks_limits.last().volume[-1] 
            row["timea"] = round((row["asks"]+1)/(last_values.volume+1),1)
            row['rangea'] = round(asks_limits.last().changes[-1],2)
        
        row["name"] = (last_values.simbol.coin_name).upper()
        row['values']=(round(last_values.volume,2))
        row['count_trades']=(last_values.count_trades)
        
        

        
        
        list_values.append(row)
        row = {'name': '', 'values':'','bids':' - ','timeb':' - ', 'rangeb': ' - ',
           'asks':' - ','timea':' - ','rangea': ' - ','count_trades':''}
        # row = {'name': '', 'values':'','bids':' - ','asks':' - ','count_trades':''}
        # row = {'name': '', 'values':'','bids':' - ','asks':' - ',}

    

    list1 = list_values[:50]
    list2 = list_values[50:100]
    list3 = list_values[100:]

    context = {'list1':list1,'list2':list2,'list3':list3}

    # send_volume_info(time.time() - start)
    return render(request, 'polls/tablev1.html', {'title': "Главная страница ", 
                    'list1':list1,'list2':list2,'list3':list3 , 'headers': headers })





def add_transaction(coin_name, volume, count_trades):
    transaction = CryptoTransaction(coin_name=coin_name, volume=volume,
                                     count_trades = count_trades)
    transaction.save()



class SimbolApiView(generics.ListAPIView):
    queryset = Simbol.objects.all()
    serializer_class = AllSimbols

class CryptoTransactionView(generics.ListAPIView):
    serializer_class = CryptoTransactionSerializer

    def get_queryset(self):
        simbol = self.kwargs['simbol']
        queryset = CryptoTransaction.objects.filter(simbol__coin_name=simbol)
        return queryset

    def get(self, request, *args, **kwargs):
        simbol = self.kwargs['simbol']
        interval = self.kwargs['interval'] # Получение значения параметра "interval" из запроса
        if interval == '1_min':
            interval_minutes = 1
        elif interval == '5_min':
            interval_minutes = 5
        elif interval == '10_min':
            interval_minutes = 10
        elif interval == '30_min':
            interval_minutes = 30
        elif interval == '1_h':
            interval_minutes = 60
        elif interval == '3_h':
            interval_minutes = 180
        elif interval == '5_h':
            interval_minutes == 300
        else:
            return Response({'error': 'Invalid interval'})

        queryset = self.get_queryset()

        data = queryset.filter(timestamp__gte=
                    datetime.now()-timedelta(
            minutes=interval_minutes)).aggregate(total_volume=Sum('volume'))
        total_volume = data['total_volume']

        return Response({interval: total_volume })

class TableViewView(generics.ListAPIView):
    serializer_class = TableViewSerializer

    def get(self, request, *args, **kwargs):
        table_name = self.kwargs["table"]
        
        headers = ['Название','Объем/мин','fshort','Вреямя','Растояние','flong','Время','Растояние',]
        if table_name == "table":
            data = TableView.objects.get(name='table').table
        elif table_name == "tableV2":
            data = TableView.objects.get(name='tableV1').table


        return Response({"data":data })
        
