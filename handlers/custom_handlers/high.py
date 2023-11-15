from loader import bot
from telebot.types import Message
from config_data.api import url, headers
import requests


@bot.message_handler(commands=['low'])
def get_low_film(message: Message):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, f'К сожалению, не удалось получить список фильмов.')

    # films = response.json()
    # print(films)
    # low_rate = max(films, key=lambda x: x['rating'])
    # print(low_rate)
