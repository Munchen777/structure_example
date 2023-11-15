from telebot.types import Message
from database.models import *
from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    user_name = message.from_user.username

    bot.reply_to(
        message, f"Добро пожаловать!\n"
                 f"Я ассистент киносайта 'Монитор'\n"
                 f"Для навигации используйте команду /help.")
            # f'Команда /low покажет вам какой фильм занимает топ в рейтинге с низким рейтингом IMDb.\n'
            # f'Команда /high - наоборот, фильм с высоким рейтингом IMDb.\n'
            # f'Команда /history покажет вам все ваши запросы.\n'


