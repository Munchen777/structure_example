from database.models import *
from handlers.custom_handlers import survey
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    find_user = User.select().where(message.from_user.id == User.telegram_id)
    if not find_user:

        bot.send_message(message.from_user.id,
                              f'🙌 Добро пожаловать, {message.from_user.username}!\n'
                              f'Я ассистент киносайта "Монитор" 🎞️.\n'
                              f'Давайте я вам вкратце расскажу о себе:\n'
                              f'я покажу, какой самый лучший и самый худший фильм/кинофильм в TOP 100 Films в рейтинге IMDb.')

        survey.survey(message=message)
    else:
        bot.send_message(message.from_user.id, f'👋 Рад вас снова видеть, {message.from_user.username}')


