# Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
import sqlite3

if __name__ == "__main__":
    # Код из предыдущего задания
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    #    создать таблицу
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
       id INTEGER PRIMARY KEY,
       username TEXT NOT NULL,
       email TEXT NOT NULL,
       age INTEGER,
       balance INTEGER NOT NULL
       )
    ''')

    #    удалить записи, если есть
    cursor.execute("DELETE FROM Users")

    #    заполнить записями
    for i in range(1, 11):
        cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,1000)",
                       (f"User{i}", f"example{i}@gmail.com", i * 10))

    #    Обновить баланс у каждой второй записи, начиная с 1-ой (установить на 500)
    # for i in range(1, 11, 2):
    #    cursor.execute("UPDATE Users SET balance=? WHERE id=?",(500, i))
    cursor.execute("UPDATE Users SET balance=? WHERE id % 2 = 1", (500,))

    #    Удалить каждую третью запись, начиная с 1-ой
    # for i in range(1, 11, 3):
    #    cursor.execute("DELETE FROM Users WHERE id=?", (i,))
    cursor.execute("DELETE FROM Users WHERE id % 3 = 1")

    # Удаление пользователя с id=6
    cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

    # Подсчёт кол-ва всех пользователей
    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]

    # Подсчёт суммы всех балансов
    cursor.execute("SELECT SUM(balance) FROM Users")
    all_balances = cursor.fetchone()[0]

    print(all_balances / total_users)

    conn.commit()
    conn.close()
