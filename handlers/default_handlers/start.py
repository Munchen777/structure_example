from telebot.types import Message
from database.models import *
from loader import bot



@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.from_user.id

    try:
        User.create(
            id=user_id
        )
        bot.reply_to(message, f'Добро пожаловать, {message.from_user.full_name}!'
                              f'Я ассистент киносайта "Монитор".')
    except IntegrityError:
        bot.reply_to(message, f'Рад вас снова видеть, {message.from_user.username}')


