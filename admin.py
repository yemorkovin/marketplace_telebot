from telebot import types
import database

def admin_menu():
    row = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Добавить товар')
    item2 = types.KeyboardButton('Просмотр заказов')
    row.add(item1, item2)
    return row

def handle_add_product(bot, message):
    msg = bot.reply_to(message, 'Введите название товара')
    bot.register_next_step_handler(msg, lambda  m: handle_product_name(bot, m))

def handle_product_name(bot, message):
    product_name = message.text
    msg = bot.reply_to(message, f'Название товара: {product_name} Введите цену товара: ')
    bot.register_next_step_handler(msg, lambda  m: handle_product_price(bot, m, product_name))

def handle_product_price(bot, message, product_name):
    price = float(message.text)
    database.add_product(product_name, price)
    bot.reply_to(message, f'Товар {product_name} с ценой {price} добавлен в каталог')



