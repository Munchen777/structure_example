import sqlite3
from database.models import *
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def user_history(message: Message):
    if not User.get(message.from_user.id == FilmInfo.user.telegram_id):
        bot.send_message(message.from_user.id, f'У вас пустая история запросов')

    history = FilmInfo.select().where(FilmInfo.user_id_for_table == message.from_user.id)

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM films""")
        print(cursor.fetchall())
    for line in history:
        bot.reply_to(message, f'{line.user.name} | {line.film_name} | {line.user_response_date_command}')

    bot.delete_state(message.from_user.id, message.chat.id)
