import User
import sqlite3


def create_user_table():
    print("Opened database successfully")

    with sqlite3.connect('royal_db.db') as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS user("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "first_name TEXT NOT NULL,"
                           "last_name TEXT NOT NULL,"
                           "username TEXT NOT NULL,"
                           "email_address TEXT NOT NULL,"
                           "address TEXT NOT NULL,"
                           "password TEXT NOT NULL)")

    print("user table created successfully")


def create_product_table():
    print("Opened database successfully")

    with sqlite3.connect('royal_db.db') as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS product("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "name TEXT NOT NULL,"
                           "description TEXT NOT NULL,"
                           "price TEXT NOT NULL,"
                           "category TEXT NOT NULL,"
                           "review TEXT NOT NULL)")

    print("user table created successfully")


def fetch_users():
    with sqlite3.connect('royal_db.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        db_users = cursor.fetchall()

        new_data = []

        for data in db_users:
            print(data)
            new_data.append(User(data[0], data[3], data[6]))
    return new_data


def insert_user(first_name, last_name, username, email_address, address, password):
    with sqlite3.connect("royal_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO user( first_name, last_name, username, email_address, address, password )"
                       f"VALUES( '{first_name}', '{last_name}', '{username}', '{email_address}', '{address}', '{password}' )")
        conn.commit()