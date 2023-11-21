import requests
from config_data.get_response import get_response
from config_data.api import url, headers
from database.get_user_info import (get_films_from_table,
                                    get_user_by_id,
                                    films_table_create)
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['low'])
def get_low_film(message: Message):
    """ Команда /low покажет вам какой фильм занимает топ в рейтинге с низким рейтингом IMDb """
    response = get_response(url, headers)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, f'😔К сожалению, не удалось получить список фильмов.')

    films = response.json()
    """ Сам фильм и его параметры """
    low_rate_film = min(films, key=lambda x: x['rating'])
    name_film = low_rate_film['title']
    user_id = message.from_user.id
    low_film_year = low_rate_film['year']
    low_film_rating = low_rate_film['rating']
    url_image = low_rate_film['image']
    film_thumbnail = low_rate_film['thumbnail']
    film_genre = low_rate_film['genre']
    film_description = low_rate_film['description']

    user = get_user_by_id(user_id=message.from_user.id)
    bot.reply_to(message, f'Уже в процессе - ищу 👀')

    films_table_create(film_name=name_film,
                       user=user.id,
                       user_id=user_id,
                       rating=low_film_rating,
                       year=low_film_year
                       )

    get_films_from_table()

    bot.send_message(message.from_user.id, f'🕵️‍♂️ Нашел для вас фильм/мультфильм с низким рейтингом IMDb Top 100.')
    bot.send_message(message.from_user.id, f'✍️Жанр фильма/мультфильма: {', '.join(film_genre)}')
    bot.send_message(message.from_user.id, f'💬Краткий сюжет и миниатюра:\n {film_description}')
    bot.send_message(message.from_user.id, film_thumbnail)
    bot.send_photo(message.from_user.id, requests.get(url_image).content)

    bot.delete_state(message.from_user.id, message.chat.id)
