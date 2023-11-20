from database.get_user_info import get_films_from_table
from database.models import *
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def user_history(message: Message):
    if not User.get(message.from_user.id == FilmInfo.user.telegram_id):
        bot.send_message(message.from_user.id, f'У вас пустая история запросов')

    history = FilmInfo.select().where(FilmInfo.user_id_for_table == message.from_user.id)

    get_films_from_table()

    for line in history:
        bot.reply_to(message, f'{line.user.name} | {line.film_name} | {line.user_response_date_command}')

    bot.delete_state(message.from_user.id, message.chat.id)
