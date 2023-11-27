import requests

from config_data.get_response import get_film_info
from database.get_user_info import (get_user_by_id,
                                    films_table_create)
from loader import bot
from telebot.types import Message
from states.contact_information import UserFilmResponse


@bot.message_handler(commands=['definite_year'])
def ask_user_to_give_a_year(message: Message):
    bot.reply_to(message, f'Пожалуйста, введите год съемки фильма,'
                          f' а я постараюсь найти такие фильмы/мультфильмы')
    bot.set_state(message.from_user.id, UserFilmResponse.film_year, message.chat.id)


@bot.message_handler(state=UserFilmResponse.film_year)
def get_year(message: Message):
    result = get_film_info(message, 'definite_year')
    if not result:
        bot.send_message(message.from_user.id, f'😔К сожалению, не удалось получить список фильмов.')
        return

    bot.reply_to(message, f'🕵️‍♀️Выполняю поиск ...')

    user = get_user_by_id(user_id=message.from_user.id)
    for film in result:
        films_table_create(film_name=film['title'],
                           user=user.id,
                           user_id=message.from_user.id,
                           rating=film['rating'],
                           year=film['year']
                           )

        bot.send_message(message.from_user.id, f'🆒Название: {film['title']}\n'
                                               f'✍️Жанр фильма/мультфильма: {', '.join(film['genre'])}\n'
                                               f'💬Краткий сюжет: {film['description']}\n'
                                               f'🔢Год выхода на экраны: {film['year']}\n'
                                               f'Изображение: ⬇️')
        bot.send_photo(message.from_user.id, requests.get(film['big_image']).content)
    bot.delete_state(message.from_user.id, message.chat.id)
