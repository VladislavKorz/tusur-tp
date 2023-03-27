from loguru import logger
from telebot import types
from django.conf import settings

from users.models import *


from bot.management.commands import custom_keyboard as ck

from bot.management.commands import geo
from bot.management.commands.bot_connection import bot


# @logger.catch
def start(message, prev_mes=False, next_mes=False, mess_id=False):
    user = Profile.objects.filter(external_id=message.chat.id).first()
    startup_project = StartUp_Profile.objects.filter(activate=True)
    if prev_mes:
        startup_project = startup_project.order_by('-viewed__create')
        startup_project_count = startup_project.count()
        startup_project = startup_project[1]
    else:
        startup_project = startup_project.exclude(viewed__isnull = False).order_by("?")
        startup_project_count = startup_project.count()
        startup_project = startup_project.first()

    if not mess_id:
        mess_id = message.message_id+1
    
    if startup_project:
        SeeStartUP.objects.get_or_create(start_up=startup_project, profile=user)
        keyboard = types.InlineKeyboardMarkup()
        previous_button = types.InlineKeyboardButton(text='<<', callback_data=f'previous_key_startup')
        next_button = types.InlineKeyboardButton(text='>>', callback_data=f'next_key_startup')
        like_button = types.InlineKeyboardButton(text='Участвовать 💚', callback_data=f'like_startup__{startup_project.pk}')
        url = settings.BASE_URL + startup_project.get_absolute_url()[1:]
        webAppTest = types.WebAppInfo(url)
        more_button = types.InlineKeyboardButton(text='Подробнее 💬', web_app=webAppTest)
        keyboard.add(like_button)
        keyboard.add(more_button)
        if startup_project_count > 1:
            keyboard.add(previous_button, next_button)
        text = f'{str(startup_project.name)}\n{str(startup_project.idea)})'
        if next_mes or prev_mes:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess_id, text=text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text, reply_markup=keyboard)

    else:
        text = "Новых стартапов не появилось\nВведите /start для возврата в меню"
        if next_mes:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess_id, text=text, reply_markup=None)
        else:
            bot.send_message(message.chat.id, text, reply_markup=None)


# @logger.catch
def start_staff(message, prev_mes=False, next_mes=False, mess_id=False):
    user = Profile.objects.filter(external_id=message.chat.id).first()
    cardProf_project = Card_Profile.objects.all().exclude(profile=user).exclude(role="I")
    if prev_mes:
        cardProf_project = cardProf_project.order_by('-viewedCard__create')
        cardProf_project_count = cardProf_project.count()
        cardProf_project = cardProf_project[1]
    else:
        cardProf_project = cardProf_project.exclude(viewedCard__isnull = False).order_by("?")
        cardProf_project_count = cardProf_project.count()
        cardProf_project = cardProf_project.first()

    if not mess_id:
        mess_id = message.message_id+1
    
    if cardProf_project:
        SeeCardProfile.objects.get_or_create(card=cardProf_project, profile=user)
        keyboard = types.InlineKeyboardMarkup()
        previous_button = types.InlineKeyboardButton(text='<<', callback_data=f'previous_key_card')
        next_button = types.InlineKeyboardButton(text='>>', callback_data=f'next_key_card')
        like_button = types.InlineKeyboardButton(text='Пригласить 💚', callback_data=f'like_card__{cardProf_project.pk}')
        keyboard.add(like_button)
        if cardProf_project.cv:
            url = settings.BASE_URL + cardProf_project.cv.url  # ЗАМЕНИТЬ НА РЕЗЮМЕ
            webAppTest = types.WebAppInfo(url)
            more_button = types.InlineKeyboardButton(text='Резюме 💬', web_app=webAppTest)
            keyboard.add(more_button)
        if cardProf_project_count > 1:
            keyboard.add(previous_button, next_button)
        text = f"Роль: {cardProf_project.get_role_display()}\n"
        text += f"Имя: {cardProf_project.profile.name}\n"
        text += f"Описание: {cardProf_project.description}\n"
        x_A = str(cardProf_project.profile.location_lat).replace(',','.')
        y_A = str(cardProf_project.profile.location_lon).replace(',','.')
        text += f"Город: {geo.get_city(x_A, y_A)}\n"
        if next_mes or prev_mes:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess_id, text=text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text, reply_markup=keyboard)

    else:
        text = "Новых экспертов не появилось\nВведите /start для возврата в меню"
        if next_mes:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess_id, text=text, reply_markup=None)
        else:
            bot.send_message(message.chat.id, text, reply_markup=None)