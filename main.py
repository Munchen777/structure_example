import logging
import handlers  # noqa
from loader import bot
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logging.basicConfig(level=logging.INFO)
    bot.infinity_polling()
