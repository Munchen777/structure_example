import requests


from config_data.get_response import get_film_info
from database.get_user_info import (get_films_from_table,
                                    get_user_by_id,
                                    films_table_create)
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['high'])
def get_low_film(message: Message):
    """ Команда /high покажет вам какой фильм занимает топ в рейтинге с высоким рейтингом IMDb. """
    result = get_film_info(message, 'high')
    if not result:
        bot.send_message(message.from_user.id, f'😔К сожалению, не удалось получить список фильмов.')
        return
    film_name, film_year, film_rating, url_image, film_thumbnail, film_genre, film_description = result

    user = get_user_by_id(user_id=message.from_user.id)
    bot.reply_to(message, f'Уже в процессе - ищу 👀')

    films_table_create(film_name=film_name,
                       user=user.id,
                       user_id=message.from_user.id,
                       rating=film_rating,
                       year=film_year
                       )

    get_films_from_table()

    bot.send_message(message.from_user.id, f'🕵️‍♂️ Нашел для вас фильм/мультфильм с высоким рейтингом IMDb Top 100.')
    bot.send_message(message.from_user.id, f'✍️Жанр фильма/мультфильма: {', '.join(film_genre)}')
    bot.send_message(message.from_user.id, f'💬Краткий сюжет и миниатюра:\n {film_description}')
    bot.send_message(message.from_user.id, film_thumbnail)
    bot.send_photo(message.from_user.id, requests.get(url_image).content)

    bot.delete_state(message.from_user.id, message.chat.id)
