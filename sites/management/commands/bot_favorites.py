from loguru import logger
from telebot import types

from bot.models import Feedback


from bot.management.commands import custom_keyboard as ck
from bot.management.commands.bot_connection import bot


@logger.catch
def start(message):
    text = 'Нажали кнопку ИЗБРАННОЕ ⭐'

    bot.send_message(message.from_user.id, text)