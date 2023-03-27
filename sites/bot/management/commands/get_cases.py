from loguru import logger

from telebot import types


from bot.models import Feedback
from users.models import StartUp_Profile, SeeStartUP, Profile


from bot.management.commands import custom_keyboard as ck
from bot.management.commands.bot_connection import bot


# @logger.catch
def start(message):
    user = Profile.objects.filter(external_id=message.from_user.id).first()
    startup_project = StartUp_Profile.objects.filter(activate=True).exclude(viewed__isnull = False).first()
    if startup_project:
        SeeStartUP.objects.get_or_create(start_up=startup_project, profile=user)
        keyboard = types.InlineKeyboardMarkup()
        previous = types.InlineKeyboardButton(text='Предыдущий',callback_data='previous')
        next_button = types.InlineKeyboardButton(text='Следующий',callback_data='next_button')
        keyboard.add(previous,next_button)
        bot.send_message(message.from_user.id, (f'{str(startup_project.name)}\n{str(startup_project.idea)})'),reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Новых стартапов не появилось")



    