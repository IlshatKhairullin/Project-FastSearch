import telebot
import Configure
from telebot import types

bot = telebot.TeleBot(Configure.config['token'])

@bot.message_handler(commands=['start'])
def start(message):
    global keyboard1

    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    search_product_price = types.KeyboardButton(text='🔎 Поиск товара')
    delivery = types.KeyboardButton(text='₽ Стоимость доставки')
    bot_help = types.KeyboardButton(text='❓ Помощь')
    keyboard1.add(search_product_price, delivery, bot_help)

    bot.send_message(message.chat.id, 'Привет, я телеграмм бот', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def callback_worker(message):
    if message.chat.type == 'private':
        if message.text == '🔎 Поиск товара':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            bot.send_message(message.chat.id, '🔎 Поиск товара', reply_markup=keyboard)

        elif message.text == '₽ Стоимость доставки':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            bot.send_message(message.chat.id, '₽ Стоимость доставки', reply_markup=keyboard)

        elif message.text == '❓ Помощь':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            bot.send_message(message.chat.id, '❓ Помощь', reply_markup=keyboard)

        if message.text == '⬅ Назад':
            bot.send_message(message.chat.id, '⬅ Назад', reply_markup=keyboard1)


bot.polling(none_stop=True, interval=0)
