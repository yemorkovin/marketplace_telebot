import sqlite3

def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("create table if not exists products (id integer primary key, name text, price real)")
    cursor.execute("create table if not exists cart (user_id integer, product_id integer, quantity integer)")
    conn.commit()
    conn.close()

def add_product(name ,price):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('insert into products (name, price) values (?, ?)', (name, price))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('select * from products')
    products = cursor.fetchall()
    conn.close()
    return products

def add_to_cart(user_id ,product_id, quantity):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('insert into cart (user_id, product_id, quantity) values (?, ?, ?)', (user_id, product_id, quantity))
    conn.commit()
    conn.close()


def get_cart(user_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('select products.name, products.price, cart.quantity from cart join products on cart.product_id = products.id where cart.user_id = ?', (user_id,))
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items


init_db()