from database.get_user_info import get_users_from_table
from database.models import *
from keyboards.inline.request_gender_inline import request_gender
from keyboards.reply.contact import get_contact
from loader import bot
from telebot.types import Message
from states.contact_information import UserInfoState


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.send_message(message.from_user.id, f'🥳Спасибо, вам за то, что согласились пройти опрос!\n'
                                           f'😸Давай знакомиться! Меня зовут Стюарт'
                                           f'Пожалуйста, укажи свое имя: ')
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    """ Принимаем от пользователя имя """
    name = message.text
    if name.isalpha():

        bot.send_message(message.from_user.id, f'👍Спасибо. Теперь введи свой возраст (от 10 до 120):')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text

    else:
        bot.send_message(message.from_user.id, f'Имя должно быть из букв!')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    """ Принимаем от пользователя возраст """
    user_age = message.text
    if user_age.isdigit():
        if int(user_age) in range(10, 121):

            bot.send_message(message.from_user.id, f'Спасибо, записал. Теперь укажи свой пол.',
                             reply_markup=request_gender())
            bot.set_state(message.from_user.id, UserInfoState.gender, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['age'] = message.text

        else:
            bot.send_message(message.from_user.id, f'Извините, вы вышли за возрастные ограничения.'
                                                   f' Введите возраст еще раз.')
    else:
        bot.send_message(message.from_user.id, f'Возраст должен состоять из цифр.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline_gender(call):
    """ Принимает от пользователя пол """
    if call.message:
        gender = call.data
        bot.send_message(call.from_user.id, f'Благодарю!',
                         reply_markup=get_contact())
        with bot.retrieve_data(call.from_user.id) as data:
            data['gender'] = call.data

        bot.set_state(call.from_user.id, UserInfoState.phone_number)


@bot.message_handler(state=UserInfoState.phone_number, content_types='contact')
def reply_callback_phone(message: Message):
    """ Принимаем номер телефона пользователя и записываем всю информацию в SqLite3 """
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id) as data:
            data['contact'] = message.contact.phone_number

        User.create(telegram_id=message.from_user.id,
                    name=data['name'],
                    age=data['age'],
                    gender=data['gender'],
                    phone=data['contact']).save()

    get_users_from_table()

    bot.reply_to(message, f'Ваш номер телефона: {data['contact']}')
    bot.delete_state(message.from_user.id, message.chat.id)
