import sqlite3

from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message
from keyboards.inline.request_gender_inline import request_gender
from keyboards.reply.contact import get_location
from database.models import *

# if not all([FilmInfo, User]):
#     db.create_tables([FilmInfo, User])

# print('Tables are created. DONE!')



@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Благодарю, вас за то, что согласились пройти опрос!'
                                           f'Пожалуйста. Введите ваше имя)')
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    name = message.text
    print(name)

    if name.isalpha():
        user_lst.append(name)
        bot.send_message(message.from_user.id, f'Спасибо. Теперь введите свой возраст.')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        #     data['name'] = message.text

    else:
        bot.send_message(message.from_user.id, f'Имя должно быть из букв!')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    user_age = message.text
    print(user_age)
    if user_age.isdigit():
        user_lst.append(user_age)
        bot.send_message(message.from_user.id, f'Спасибо, записал. Теперь введи свой пол.',
                         reply_markup=request_gender())
        bot.set_state(message.from_user.id, UserInfoState.gender, message.chat.id)
        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        #     data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Возраст состоит из цифр.')


# @bot.message_handler(state=UserInfoState.gender)
# def get_gender(message) -> None:
#
#     if message.text.isalpha():
#         if message.text == 'мужской':
#             bot.reply_to(message, f'Какое у вас благородное имя.')
#         if message.text == 'женский':
#             bot.reply_to(message, f'Какое у вас красивое имя, как и вы)')
#         User.gender = message.text
#         bot.send_message(message.from_user.id, f'Спасибо, записал.')
#         bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['gender'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, f'Имя должно быть из букв!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline_gender(call):
    print(call.data)
    if call.message:
        gender = call.data
        bot.send_message(call.from_user.id, f'Благодарю!',
                         reply_markup=get_location())
        # with bot.retrieve_data(call.from_user.id, call.chat.id) as data:
        #     data['gender'] = call.data
        user_lst.append(gender)
        bot.set_state(call.from_user.id, UserInfoState.phone_number)


@bot.message_handler(state=UserInfoState.phone_number, content_types='contact')
def reply_callback_phone(message: Message):
    if message.content_type == 'contact':
        # with bot.retrieve_data(message.from_user.id) as data:
        #     data['contact'] = message.contact.phone_number

        user_lst.append(message.contact.phone_number)
        User.create(name=user_lst[0],
                    age=user_lst[1],
                    gender=user_lst[2],
                    phone=message.contact.phone_number).save()

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users""")
        print(cursor.fetchall())
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(message, f'Ваш номер телефона: {user_lst[3]}')





user_lst = list()
