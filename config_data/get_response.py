import requests


from config_data.api import url, headers
from loader import bot
from telebot.types import Message


def get_film_info(message: Message, from_module: str):
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        return False
    films = response.json()
    if from_module == 'low':
        """ Берем информацию для реализации команды /low """
        current_film_rate = min(films, key=lambda x: x['rating'])
        film_name = current_film_rate['title']
        film_year = current_film_rate['year']
        film_rating = current_film_rate['rating']
        url_image = current_film_rate['image']
        film_thumbnail = current_film_rate['thumbnail']
        film_genre = current_film_rate['genre']
        film_description = current_film_rate['description']
        return (film_name, film_year, film_rating, url_image, film_thumbnail,
                film_genre, film_description)

    elif from_module == 'high':
        """ Берем информацию для реализации команды /high """
        current_film_rate = max(films, key=lambda x: x['rating'])
        film_name = current_film_rate['title']
        film_year = current_film_rate['year']
        film_rating = current_film_rate['rating']
        url_image = current_film_rate['image']
        film_thumbnail = current_film_rate['thumbnail']
        film_genre = current_film_rate['genre']
        film_description = current_film_rate['description']
        return (film_name, film_year, film_rating, url_image, film_thumbnail,
                film_genre, film_description)

    elif from_module == 'definite_year':
        """ Берем информацию для реализации команды /definite_year """
        user_year = int(message.text)
        films_with_such_year = list(filter(lambda elem: elem['year'] == user_year, films))
        if not films_with_such_year:
            bot.reply_to(message, f'🤷К сожалению, фильм с годом съемки {user_year} года не найден.')
            return
        return films_with_such_year
