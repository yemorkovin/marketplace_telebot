import telebot
from telebot import types
from config import TOKEN, ADMIN_ID
import database
from admin import admin_menu, handle_add_product, handle_product_name, handle_product_price

bot = telebot.TeleBot(TOKEN)

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Каталог')
    itembtn2 = types.KeyboardButton('Корзина')
    markup.add(itembtn1, itembtn2)
    return markup

# Команда старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в наш интернет-магазин!", reply_markup=main_menu())

# Команда для администратора
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == int(ADMIN_ID):
        bot.reply_to(message, "Добро пожаловать в админ-панель!", reply_markup=admin_menu())
    else:
        bot.reply_to(message, "У вас нет доступа к этой команде.")

# Показать каталог
@bot.message_handler(func=lambda message: message.text == 'Каталог')
def show_catalog(message):
    products = database.get_products()
    if products:
        for product in products:
            bot.send_message(message.chat.id, f"{product[1]} - {product[2]} руб.", reply_markup=add_to_cart_button(product[0]))
    else:
        bot.send_message(message.chat.id, "Каталог пуст.")

# Добавить в корзину кнопка
def add_to_cart_button(product_id):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Добавить в корзину", callback_data=f"add_to_cart:{product_id}")
    markup.add(button)
    return markup

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart'))
def callback_inline(call):
    product_id = int(call.data.split(':')[1])
    database.add_to_cart(call.from_user.id, product_id, 1)
    bot.answer_callback_query(call.id, "Товар добавлен в корзину")
    bot.send_message(call.message.chat.id, "Товар добавлен в корзину")

# Показать корзину
@bot.message_handler(func=lambda message: message.text == 'Корзина')
def show_cart(message):
    cart_items = database.get_cart(message.from_user.id)
    if cart_items:
        total = 0
        for item in cart_items:
            bot.send_message(message.chat.id, f"{item[0]} - {item[2]} шт. - {item[1]*item[2]} руб.")
            total += item[1] * item[2]
        bot.send_message(message.chat.id, f"Общая сумма: {total} руб.")
    else:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")

# Обработчики для админских команд
@bot.message_handler(func=lambda message: message.text == 'Добавить товар' and message.from_user.id == int(ADMIN_ID))
def add_product(message):
    handle_add_product(bot, message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
