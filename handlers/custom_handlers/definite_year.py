import requests
from config_data.api import url, headers
from database.get_user_info import get_user_by_id
from database.models import *
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
    user_year = int(message.text)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, f'😔К сожалению, не удалось получить список фильмов.')

    films_lst = response.json()
    bot.reply_to(message, f'🕵️‍♀️Выполняю поиск ...')
    films_with_such_year = list(filter(lambda elem: elem['year'] == user_year, films_lst))
    if not films_with_such_year:
        bot.reply_to(message, f'🤷К сожалению, фильм с годом съемки {user_year} года не найден.')

    user = get_user_by_id(user_id=message.from_user.id)
    for film in films_with_such_year:
        FilmInfo.create(
            film_name=film['title'],
            user=user.id,
            user_id_for_table=message.from_user.id,
            film_rating=film['rating'],
            film_year=film['year']
        ).save()
        film_genre = film['genre']
        bot.send_message(message.from_user.id, f'🆒Название: {film['title']}\n'
                                               f'✍️Жанр фильма/мультфильма: {', '.join(film_genre)}'
                                               f'💬Краткий сюжет: {film['description']}\n'
                                               f'Изображение: ⬇️')
        bot.send_photo(message.from_user.id, requests.get(film['big_image']).content)
    bot.delete_state(message.from_user.id, message.chat.id)
