from peewee import *
from config_data.config import DB_PATH
import datetime
db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    id = AutoField()
    """ Базовый класс. """

    class Meta:
        database = db


class User(BaseModel):
    # 1.Имя
    # 2.Возраст
    # 3.Пол
    # 4.Время и дата обращения пользователя
    """ Дочерний класс таблицы Пользователя"""
    name = CharField(max_length=150)
    age = IntegerField()
    gender = CharField()
    users_response_time = DateTimeField(default=datetime.datetime.now,
                                        formats='%b-%d-%Y %H:%M:%S')
    phone = CharField()
    
    class Meta:
        db_table = 'users'


class FilmInfo(BaseModel):
    #1.Название фильма
    #2.Фильмы пользователя
    #3.Рейтинг фильма
    #4.Год выпуска фильма
    #5.Дата для history (хочу сделать так: как пользователь /
    # введет команду /low, /high, /custom(введет год и дальше ему покажется фильм)/
    # чтобы дата этого обращения записалась в бд, для отражения истории запросов

    """ Дочерний класс таблицы Фильм """
    # Смогу получить фильмы пользователя user.films
    film_name = CharField()
    user = ForeignKeyField(User, backref='films')
    user_id_for_table = CharField()
    film_rating = FloatField()
    film_year = IntegerField()
    user_response_date_command = DateTimeField(default=datetime.datetime.now,
                                               formats="%b-%d-%Y %H:%M:%S")

    class Meta:
        db_table = 'films'

    def __str__(self):
        return "{film_id} - {film_name} - {date_response}".format(
            film_id=self.id,
            film_name=self.film_name,
            date_response=self.user_response_date_command
        )


db.create_tables([User, FilmInfo])
print('Таблицы созданы')




