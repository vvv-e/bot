# Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
# Домашнее задание по теме "Написание примитивной ORM"

import sqlite3


def initiate_db():
    # Код из предыдущего задания
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    # создать таблицу Products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
       id INTEGER PRIMARY KEY,
       title TEXT NOT NULL,
       description TEXT,
       price INTEGER NOT NULL
       )
    ''')
    # создать таблицу Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
       id INTEGER PRIMARY KEY,
       username TEXT NOT NULL,
       email TEXT NOT NULL,
       age INTEGER NOT NULL,
       balance INTEGER NOT NULL
       )
    ''')
    conn.commit()
    conn.close()


def get_all_products():
    # Выборку всех записей при помощи fetchall(), где возраст не равен 60
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, price FROM Products ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_user(username, email, age):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,1000)",
                   (username, email, age))
    conn.commit()
    conn.close()


def is_included(username):
    # Выборку всех записей при помощи fetchall(), где возраст не равен 60
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    exist = cursor.execute("SELECT username FROM Users WHERE username=?", (username,)).fetchone()
    conn.close()
    return not exist is None


if __name__ == "__main__":
    # создать таблицу Products
    initiate_db()
    # создать 4 записи
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    # удалить записи, если есть
    cursor.execute("DELETE FROM Products")
    # заполнить записями
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   ("Ручка перьевая", "Производитель LAMY", 3000))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   ("Пинцет", "Made in Pakistan", 500))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   ("Нож канцелярский", "Силумин, сталь. Сделано в КНР", 1000))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   ("Ножницы для бумаги", "Производитель Zinger", 2000))
    conn.commit()
    conn.close()
    # проверить работоспособность модулей для Users
    add_user("vvve", "vvve@gmail.com", 56)
    print(is_included("vvve"))
    # удалить результаты проверки
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    # удалить записи, если есть
    cursor.execute("DELETE FROM Users")
    conn.commit()
    conn.close()
