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
