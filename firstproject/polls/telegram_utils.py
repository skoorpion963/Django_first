import telebot

# Здесь необходимо указать ваш токен бота
TOKEN = '6186704817:AAHtjmNLjvaOxycmgtn5XyBbs7i6UUiczx8'
bot = telebot.TeleBot(TOKEN)


# # Обработка команды /start
# @bot.message_handler(commands=['start'])
# def start(message):
#     # Разделение текста на аргументы команды
#     args = message.text.split()

#     # Проверка наличия параметра
#     if len(args) > 1:
#         param_value = args[1]
#         bot.reply_to(message, f'Привет! Ты перешел по ссылке с параметром {param_value}.')
#     else:
#         bot.reply_to(message, 'Привет! Ты перешел по ссылке без параметра.')


# # Запуск бота
# bot.polling()

# 474298822



# @bot.message_handler()
# def handle_message(message):
#     chat_id = message.chat.id
#     print("Received message from chat ID:", chat_id)
#     # Дополнительные действия, которые вы можете выполнить с полученным ID чата


# bot.polling()
def send_info(text):
    TOKEN = '6186704817:AAHtjmNLjvaOxycmgtn5XyBbs7i6UUiczx8'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(474298822,text)

def test():
    TOKEN = '6186704817:AAHtjmNLjvaOxycmgtn5XyBbs7i6UUiczx8'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(474298822,'попа')



