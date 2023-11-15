from telebot.handler_backends import State, StatesGroup
from telebot.types import Contact


class UserInfoState(StatesGroup):
    """ Состояния пользователя для последовательного получения данных """
    name: str = State()
    age: int = State()
    gender: str = State()
    country: str = State()
    phone_number: Contact = State()
