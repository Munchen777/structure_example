import re
from config_data.config import RESPONSE_WELCOME_PHRASES
from loader import bot
from telebot.types import Message


# Эхо-хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    """ Если в слово-приветствие, то приветствуем в ответ, а иначе помогаем разобраться """
    answer_hello = (re.findall(r'[пП]ривет', message.text)
                    or re.findall(r'[hH]ello', message.text))
    if answer_hello:
        bot.send_message(message.from_user.id,
                         RESPONSE_WELCOME_PHRASES['hello']['say_hello'].format(
                             username=message.from_user.username))
    else:
        bot.send_message(
            message.from_user.id,
            RESPONSE_WELCOME_PHRASES['hello']['helping_phrase'])
