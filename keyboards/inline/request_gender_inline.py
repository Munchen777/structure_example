from loader import bot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def request_gender():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Мужской', callback_data='мужской'),
               InlineKeyboardButton('Женский', callback_data='женский'))

    return markup
