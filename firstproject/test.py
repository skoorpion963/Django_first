
import requests

r = requests.get("http://www.cscalphelper.ru/api/v1/table/")

print(r.json)


import matplotlib.pyplot as plt
import requests


"sklusdt"
"dydxusdt"
"egldusdt"
simbol  = "wavesusdt"
diph = requests.get(f'https://fapi.binance.com/fapi/v1/depth?symbol={simbol.upper()}&limit=1000').json()
asks_list = []
bids_list = []
for i in diph['asks']:
    if len(asks_list) < 200:
        asks_list.append(i) 

for i in diph['bids']:
    if len(bids_list) < 200:
        bids_list.append(i)



bids_list = bids_list
asks_list = asks_list
# Разделение списка на два отдельных списка (цены и количество)
prices = [item[0] for item in bids_list]
quantities = [float(item[1]) for item in bids_list]

# Создание графика
plt.barh(prices, quantities)

# # Настройка осей
# plt.xticks(range(len(diph_list)), prices)
plt.xlabel('Количество')
plt.ylabel('Цены')

# Отображение графика
plt.show()
prices = [item[0] for item in asks_list]
quantities = [float(item[1]) for item in asks_list]

# Создание графика
plt.barh(prices, quantities)

# # Настройка осей
# plt.xticks(range(len(diph_list)), prices)
plt.xlabel('Количество')
plt.ylabel('Цены')

# Отображение графика
plt.show()

