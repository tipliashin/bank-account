import sqlite3

# Подключаемся к базе (если файла нет, он создастся)
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS accounts")
# Создаём таблицу
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        balance REAL DEFAULT 0.0
    )
''')

# Вставляем данные
cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", ('Анна', 500.0))
cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", ('Иван', 300.0))
cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", ('Андрей', 168423.3))
cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", ('Кристина', 11233123300.0))

# Сохраняем изменения (обязательно!)


# Делаем запрос

cursor.execute("SELECT * FROM accounts WHERE balance > 100")
rows = cursor.fetchall()
for row in rows:
    print(row)  # каждая строка — кортеж
cursor.execute("UPDATE accounts SET balance = 1 WHERE owner = 'Андрей'")
cursor.execute("DELETE FROM accounts WHERE id = 2")
cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()

conn.commit()

for row in rows:
    print(row)  # каждая строка — кортеж

# Закрываем соединение
conn.close()
