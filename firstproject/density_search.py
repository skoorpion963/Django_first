import requests
import ccxt
from requests.exceptions import ConnectionError
from django.utils import timezone
from polls.models import CryptoTransaction , BigLimits ,\
    Simbol , BigLimitsEz 




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
        
        # send_volume_info(f'Крупная заявка {simbol} количество монет: {volume} цена:{price} расстояние:{difference}')
        
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
    # print(f'Изменение крупной заявки {big_limits[0].simbol.coin_name} , id = {big_limits[0].id}')


    

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
            
            # print(f"Крупная заявка ,на покупку {simbol} :" , asks_ansver[0],asks_ansver[1], " Дальность : ","%.2f" % range,'%' )
            # print("Привышение суммы объема в стакане до заявки на  ",difference ,' %')


    if bids_ansver != []:
        range = float(simbol_book_depth['bids'][0][0])/float(bids_ansver[0])*100-100
        difference = float(bids_ansver[1])/(float(bids_ansver[2])-float(bids_ansver[1]))*100-100
        if range > 0.1 and range < 200:
            sheck_big_limits(simbol=simbol,volume=bids_ansver[1],price=bids_ansver[0],difference=range,is_purchase=False, my_dict =bids_dict)
            
            # print(f"Крупная заявка ,на продажу {simbol} :" , bids_ansver[0],bids_ansver[1], " Дальность : ","%.2f" % range,'%' )
            # print("Привышение суммы объема в стакане до заявки на  ",difference ,' %')

        
    

def main():
    simbols  = get_simbol_names()
    print(len(simbols))
    while True:
        
        for simbol in simbols:
            
            order_book = get_order_book(simbol=simbol)
            simbol_volues = get_simbol_volume(simbol=simbol)
            
            if len(order_book)!= 2 and simbol_volues !=0:
                density_search_1(
                    simbol_volume = sum(simbol_volues)/len(simbol_volues),
                    simbol_book_depth = order_book,
                    simbol = simbol,
                )

main()
