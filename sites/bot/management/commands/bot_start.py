from django.conf import settings
from loguru import logger

import telebot
import datetime
from telebot import types

from bot.management.commands import custom_keyboard as ck
from bot.management.commands import users_register
from bot.management.commands import get_feedback
from bot.management.commands import get_cases
from bot.management.commands import bot_notifical
from bot.management.commands import bot_favorites
from bot.management.commands import bot_search
from bot.management.commands.bot_connection import bot

from users.models import *


logger.debug('START BOT')

# @logger.catch
@bot.message_handler(commands=['start', 'sign_up'])
def start_message(message):
    profile, isCreated = Profile.objects.get_or_create(external_id = message.from_user.id)
    profile.activate = True
    profile.username = message.from_user.username
    profile.save()
    answer = "Добро пожаловать!"
    if message.text == '/sign_up':
        if not isCreated:
            answer = "Вы уже зарегистрированы"
            bot.send_message(message.from_user.id, answer, reply_markup=ck.start_keyboard)
        else:
            users_register.sign_up(message)
    elif message.text == '/start':
        if not isCreated:
            send_main_menu(message.from_user.id)
        else:
            users_register.sign_up(message)
    else:
        bot.send_message(message.from_user.id, "Не смогли Вас понять, повторите запрос", reply_markup=ck.deleted_keyboard)
        

def send_main_menu(user_id):
    answer = "Выберите куда перейти дальше?"
    bot.send_message(user_id, answer, reply_markup=ck.main_menu_keyboard(user_id))


@bot.message_handler(commands=['statistics'])
def get_statistic(message):
    msg = f"Количество пользователей: {Profile.get_statistic()}\nКоличество стартапов: {StartUp_Profile.get_statistic()}\nКоличество отмодерированых стартапов: {StartUp_Profile.get_all_moderated_startups()}\nКоличество карт экспертов: {Card_Profile.get_statistic()}\n"
    bot.send_message(message.from_user.id,msg)

# @logger.catch
@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == "Главное Меню":
        send_main_menu(message.from_user.id)
    elif message.text == "Найти стартап 🔎":
        bot_search.start(message)
    elif message.text == "Найти команду 🔎":
        bot_search.start_staff(message)
    elif message.text == "Уведомления 🔔":
        bot_notifical.start(message)
    elif message.text == "Избранное ⭐":
        bot_favorites.start(message)
    elif message.text == "Написать в BizDate ⚙️":
        bot.send_message(message.from_user.id, 'Разработкой проекта занимается команда КуйКод.\nВсе интересующие Вас вопросы и предложения, Вы можете задать в сообщения - @vkorzhovv')
    else:
        logger.error(f'Получили сообщение от пользователя @{message.from_user.username} {message.from_user.id} не смогли его распознать: {message.text}')

@bot.message_handler(content_types="web_app_data") 
def answer(webAppMes):
    if webAppMes.web_app_data.data == "startUp_create":
        bot.send_message(webAppMes.chat.id, f"Стартап успешно создан и ожидает свою команду✅") 
    elif webAppMes.web_app_data.data == "cardProfile_create":
        bot.send_message(webAppMes.chat.id, f"Карточку профиля успешно создали✅") 
    else:
        logger.error(f'Получили web_app_data не смогли его распознать: {webAppMes}')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "phone":
        users_register.contact(call)
    elif call.data == "escape":
        send_main_menu(call.from_user.id)
    elif call.data == "signIn_key":
        bot.send_message(call.from_user.id, 'Нажали кнопку войти')
    elif call.data == "signOut_key":
        bot.send_message(call.from_user.id, 'Нажали кнопку выйти')
    elif call.data == "registration_key":
        users_register.sign_up(call)
    elif call.data == "cases_key":
        get_cases.start(call)
    elif call.data == "feedback_key":
        get_feedback.start(call)
    elif call.data == "previous_key_startup":
        bot_search.start(call.message, prev_mes=True, mess_id=call.message.message_id)
    elif call.data == "next_key_startup":
        bot_search.start(call.message, next_mes=True, mess_id=call.message.message_id)
    elif call.data == "previous_key_card":
        bot_search.start_staff(call.message, prev_mes=True, mess_id=call.message.message_id)
    elif call.data == "next_key_card":
        bot_search.start_staff(call.message, next_mes=True, mess_id=call.message.message_id)
    elif "match_" in call.data:
        match_list = str(call.data).split('_')
        logger.debug(match_list)
        if len(match_list) == 4:
            card = Card_Profile.objects.get(pk = match_list[2])
            startup = StartUp_Profile.objects.get(pk = match_list[3])
            match, _ = DatingCard_StartUp.objects.get_or_create(card=card, start_up=startup)
            if match_list[1] == 'R':
                match.match_profile = True
                match.match_profile_datetime = datetime.datetime.now()
            else:
                logger.error(match_list[1])
                match.match_start_up = True
                match.match_start_up_datetime = datetime.datetime.now()
            match.save()
            text = f"Отклик \"{card.profile.name}\" отправлен 💚"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, reply_markup=None)
        elif len(match_list) == 2:
            match = DatingCard_StartUp.objects.get(pk=int(match_list[1]))
            match.match_start_up = True
            match.save()
    elif "like_startup__" in call.data:
        sartup_pk = call.data.replace("like_startup__", "")
        user_obj = Profile.objects.get(external_id=call.from_user.id)
        if user_obj.card.all():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text, reply_markup=ck.get_role_keyboard(user_obj.card.all(), sartup_pk))
        else:
            text = "Для отклика на StartUp создайте карточку!"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, reply_markup=ck.create_role_keyboard(call.from_user.id))
    elif "like_card__" in call.data:
        user_pk = call.data.replace("like_card__", "")
        user_obj = Profile.objects.get(external_id=call.from_user.id)
        if user_obj.startUp_user.all():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text, reply_markup=ck.get_startUp_keyboard(user_obj.startUp_user.all(), user_pk))
        else:
            text = "Для приглашения пользователя в команду, создайте StartUp!"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, reply_markup=None)
    elif call.data == "next_button":
        user = Profile.objects.filter(external_id=call.message.from_user.id).first()
        startup_project = StartUp_Profile.objects.filter(activate=True).exclude(viewed__isnull = False).first()
        if startup_project:
            SeeStartUP.objects.get_or_create(start_up=startup_project, profile=user)    
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'{str(startup_project.name)}\n{str(startup_project.idea)})')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Новых сообщений нет!')
    else:
        logger.error(f'Получили callback не смогли его распознать:\ncall.data: {call.data}\ncall: {call}\n')
    bot.answer_callback_query(call.id)

bot.infinity_polling()

logger.debug('STOP BOT')