from .models import User, FilmInfo


def get_user_by_id(user_id):
    return (User
            .get(User.telegram_id == user_id)
            )


def get_users_from_table():
    """ Печатаем информацию о пользователях """
    users_data = User.select()
    for user in users_data:
        print(f'{user.name} | {user.telegram_id} | {user.age} |'
              f' {user.phone} | {user.gender} | {user.users_response_time}')


def get_films_from_table():
    """ Печатаем информацию о фильмах """
    films_data = FilmInfo.select()
    for film in films_data:
        print(f'{film.film_name} | {film.user.telegram_id} | {film.film_rating} |'
              f' {film.film_year} | {film.user_response_date_command}')


def check_user_id_in_films_table(message_id):
    """ Проверяем на наличие telegram_id в таблице "фильмы" """
    return (User
            .get(message_id == FilmInfo.user.telegram_id)
            )


def films_table_create(film_name, user, user_id, rating, year):
    """ Создаем таблицу в "фильмах" с соответствующими полями """
    FilmInfo.create(
        film_name=film_name,
        user=user,
        user_id_for_table=user_id,
        film_rating=rating,
        film_year=year
    ).save()
