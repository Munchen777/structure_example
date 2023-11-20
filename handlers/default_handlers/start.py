from config_data.config import RESPONSE_TEMPLATES
from database.models import *
from handlers.custom_handlers import survey
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    find_user = User.select().where(message.from_user.id == User.telegram_id)
    if not find_user:

        bot.send_message(message.from_user.id, RESPONSE_TEMPLATES['start_message']['new_user'].format(
            username=message.from_user.username
        )
    )
        survey.survey(message=message)
    else:
        bot.send_message(message.from_user.id, RESPONSE_TEMPLATES['start_message']['regular_user'].format(
            username=message.from_user.username
        )
    )
