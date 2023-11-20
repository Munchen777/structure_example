import sqlite3
from .models import User, DB_PATH


def get_user_by_id(user_id):
    return (User
            .get(User.telegram_id == user_id)
            )


def get_users_from_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users""")
        print(cursor.fetchall())


def get_films_from_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM films""")
        print(cursor.fetchall())