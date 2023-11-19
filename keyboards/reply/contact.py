from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_contact() -> ReplyKeyboardMarkup:
    """ Кнопка для получения номера телефона пользователя """
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text='Пожалуйста, отправьте свой номер телефона',
                                request_contact=True))
    return keyboard
