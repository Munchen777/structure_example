import requests


from config_data.api import url, headers
from loader import bot
from telebot.types import Message


def get_current_film_info_from_command(current_film):
    return (
        current_film['title'],
        current_film['year'],
        current_film['rating'],
        current_film['image'],
        current_film['thumbnail'],
        current_film['genre'],
        current_film['description']
    )


def get_film_info(message: Message, from_module: str):
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        return False

    films = response.json()
    if from_module == 'low':
        """ Берем информацию для реализации команды /low """
        current_film_rate = min(films, key=lambda x: x['rating'])
        current_result = get_current_film_info_from_command(current_film_rate)
        return current_result

    elif from_module == 'high':
        """ Берем информацию для реализации команды /high """
        current_film_rate = max(films, key=lambda x: x['rating'])
        current_result = get_current_film_info_from_command(current_film_rate)
        return current_result

    elif from_module == 'definite_year':
        """ Берем информацию для реализации команды /definite_year """
        user_year = int(message.text)
        films_with_such_year = list(filter(lambda elem: elem['year'] == user_year, films))
        if not films_with_such_year:
            bot.reply_to(message, f'🤷К сожалению, фильм с годом съемки {user_year} года не найден.')
            return
        return films_with_such_year
