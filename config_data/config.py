import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота."),
    ("help", "Вывести справку."),
    ('survey', 'Опрос.'),
    ('history', 'Ваша история запросов.'),
    ('low', 'Фильм с наименьшим рейтингом IMDb.'),
    ('high', 'Фильм с наивысшим рейтингом IMDb.'),
    ('definite_year', 'Фильм с определенным годом съемки.')
)
DB_PATH = 'database.db'

RESPONSE_TEMPLATES = {
    'start_message':
        {'new_user':
            '🙌 Добро пожаловать, {username}!\n'
            'Я ассистент киносайта "Монитор" 🎞️.\n'
            'Давайте я вам вкратце расскажу о себе:\n'
            'я покажу, какой самый лучший и самый худший фильм/кинофильм'
            ' в TOP 100 Films в рейтинге IMDb.',
         'regular_user': '👋 Рад вас снова видеть, {username}!'
         }
}

RESPONSE_WELCOME_PHRASES = {
    'hello':
        {'say_hello':
            'Рад вас видеть, дорогая/ой {username}!',
         'helping_phrase':
            f'Вы заблудились?\n'
            f'ℹ️Для навигации используйте команду /help. 🙋‍'
         }
}