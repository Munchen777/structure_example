from config_data.config import DEFAULT_COMMANDS
from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    bot.send_message(message.from_user.id, f'Вот все мои возможности: ⬇️')
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
