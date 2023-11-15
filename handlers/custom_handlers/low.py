import sqlite3

from loader import bot
from telebot.types import Message
from config_data.api import url, headers
import requests
from database.models import *
from PIL import Image
from urllib.request import urlopen


@bot.message_handler(commands=['low'])
def get_low_film(message: Message):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, f'К сожалению, не удалось получить список фильмов.')

    films = response.json()
    # print(films)
    low_rate_film = min(films, key=lambda x: x['rating'])
    name_film = low_rate_film['title']
    # print(low_rate)
    FilmInfo.create(
        film_name=name_film,
        user_id_for_table=message.from_user.id
    ).save()
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM films""")
        print(cursor.fetchall())
    # low_film_url = low_rate['image']
    # image = open(low_film_url, 'wb')
    # image.write(low_film_url.content)

    # print(low_rate)


