from telebot.types import ReplyKeyboardMarkup, KeyboardButton
#
#
# def request_gender() -> ReplyKeyboardMarkup:
#     keyboard = ReplyKeyboardMarkup(True, True)
#     keyboard.add('Мужской', 'Женский')
#     return keyboard

def get_location() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Пожалуйста, отправьте свой номер телефона',
                                request_contact=True))
    return keyboard
