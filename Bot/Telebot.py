import time
import telebot
import Configure
from telebot import types
from Parsers.United_parsers import combine_parsers

bot = telebot.TeleBot(Configure.config['token'])

@bot.message_handler(commands=['help', 'start'])
def start(message):
    global keyboard1

    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    address = types.KeyboardButton(text='Адрес доставки')
    search_product_price = types.KeyboardButton(text='🔎 Поиск товара')
    delivery = types.KeyboardButton(text='₽ Стоимость доставки')
    bot_help = types.KeyboardButton(text='❓ Помощь')
    keyboard1.add(address, search_product_price, delivery, bot_help)

    bot.send_message(message.chat.id, 'Привет, я телеграмм бот', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def callback_worker(message):
    global flag
    if message.chat.type == 'private':
        if message.text == '🔎 Поиск товара':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)
            bot.send_message(message.chat.id, '🔎 Поиск товара')

            product_name = bot.send_message(message.chat.id, 'Введите название продукта', reply_markup=keyboard)  # чтобы вернуться надо 2 раза нажать назад - пофиксить
            bot.register_next_step_handler(product_name, product_info_func)
            flag = 1
            waitMethod()

            bot.send_message(message.chat.id, prod_info)

        elif message.text == 'Адрес доставки':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            user_address = bot.reply_to(message, 'Введите пожалуйста адрес доставки')
            bot.register_next_step_handler(user_address, handle_address)

            # bot.send_message(message.chat.id, 'Теперь вы можете перейти к вводу товара')

        elif message.text == '₽ Стоимость доставки':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            bot.send_message(message.chat.id, '₽ Стоимость доставки', reply_markup=keyboard)

        elif message.text == '❓ Помощь':  # прописать в помощь, что сначала нужно ввести адрес доставки
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅ Назад')
            keyboard.add(back)

            bot.send_message(message.chat.id, '❓ Помощь', reply_markup=keyboard)

        if message.text == '⬅ Назад':
            bot.send_message(message.chat.id, '⬅ Назад', reply_markup=keyboard1)

def waitMethod():
    while True:
        if flag == 1:
            time.sleep(5)
        else:
            break

def handle_address(user_address):
    global address
    address = user_address.text

def product_info_func(product_name):
    global prod_info, flag
    prod_info = f'Найдено несколько вариантов\n{combine_parsers(product_name.text, address)}'
    flag = 0
    return


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
