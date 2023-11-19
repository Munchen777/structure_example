import requests
import sqlite3
from config_data.api import url, headers
from database.models import *
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['high'])
def get_low_film(message: Message):
    """ Команда /high покажет вам какой фильм занимает топ в рейтинге с высоким рейтингом IMDb. """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, f'К сожалению, не удалось получить список фильмов.')

    films = response.json()
    """ Сам фильм и его параметры """
    high_rate_film = max(films, key=lambda x: x['rating'])
    name_film = high_rate_film['title']
    user_id = message.from_user.id
    high_film_year = high_rate_film['year']
    high_film_rating = high_rate_film['rating']
    url_image = high_rate_film['image']
    film_thumbnail = high_rate_film['thumbnail']
    film_genre = high_rate_film['genre']
    film_description = high_rate_film['description']

    user = User.get(User.telegram_id == message.from_user.id)
    bot.reply_to(message, f'Уже в процессе - ищу 👀')

    FilmInfo.create(
        film_name=name_film,
        user=user.id,
        user_id_for_table=user_id,
        film_rating=high_film_rating,
        film_year=high_film_year
    ).save()
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM films""")
        print(cursor.fetchall())

    bot.send_message(message.from_user.id, f'🕵️‍♂️ Нашел для вас фильм/мультфильм с высоким рейтингом IMDb Top 100.')
    bot.send_message(message.from_user.id, f'✍️Жанр фильма/мультфильма: {', '.join(film_genre)}')
    bot.send_message(message.from_user.id, f'💬Краткий сюжет и миниатюра:\n {film_description}')
    bot.send_message(message.from_user.id, film_thumbnail)
    bot.send_photo(message.from_user.id, requests.get(url_image).content)

    bot.delete_state(message.from_user.id, message.chat.id)

