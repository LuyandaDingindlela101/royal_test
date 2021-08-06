import sqlite3

database_name = "radical_store"


#   FUNCTION WILL CREATE THE USER TABLE
def create_user_table():
    with sqlite3.connect(database_name) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS user("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "first_name TEXT NOT NULL,"
                           "last_name TEXT NOT NULL,"
                           "username TEXT NOT NULL,"
                           "email_address TEXT NOT NULL,"
                           "address TEXT NOT NULL,"
                           "password TEXT NOT NULL)")

    print("user table created successfully")


#   FUNCTION WILL CREATE THE PRODUCT TABLE
def create_product_table():
    with sqlite3.connect(database_name) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS product("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "name TEXT NOT NULL,"
                           "description TEXT NOT NULL,"
                           "price TEXT NOT NULL,"
                           "category TEXT NOT NULL,"
                           "review TEXT NOT NULL)")

    print("user table created successfully")


#   FUNCTION WILL GET ALL THE USERS IN THE DATABASE AND RETURN THEM
def get_users():
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user")

        return cursor.fetchall()


#   FUNCTION WILL REGISTER A NEW USER
def register_user(first_name, last_name, username, email_address, address, password):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO user( first_name, last_name, username, email_address, address, password )"
                       f"VALUES( '{first_name}', '{last_name}', '{username}', '{email_address}', '{address}', '{password}' )")
        connection.commit()


#   FUNCTION WILL LOG A REGISTERED USER IN
def get_user(username, password):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")

        return cursor.fetchone()


#   FUNCTION WILL SAVE A PRODUCT TO THE DATABASE
def save_product(name, description, price, category, review):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO product( name, description, price, category, review )"
                       f"VALUES( '{name}', '{description}', '{price}', '{category}', '{review}' )")

        connection.commit()


#   FUNCTION WILL GET ALL THE PRODUCTS FROM THE DATABASE AND RETURN THEM
def get_all_products():
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product")

        return cursor.fetchall()


#   FUNCTION WILL GET A PRODUCT FROM THE DATABASE WHICH MATCHES THE PROVIDED ID
def get_one_product(product_id):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM product WHERE id={str(product_id)}")

        return cursor.fetchone()


#   FUNCTION WILL DELETE A PRODUCT FROM THE DATABASE WHICH MATCHES THE PROVIDED ID
def delete_product(product_id):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM product WHERE id={str(product_id)}")

        connection.commit()


#   FUNCTION WILL EDIT A PRODUCT FROM THE DATABASE WHICH MATCHES THE PROVIDED ID
def update_product(row_name, new_value, product_id):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE product SET {row_name} = '{str(new_value)}' WHERE id = {str(product_id)}")

        connection.commit()
