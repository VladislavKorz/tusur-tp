from loguru import logger

from telebot import types


from users.models import StartUp_Profile, Profile


from bot.management.commands import custom_keyboard as ck
from bot.management.commands.bot_connection import bot


def sign_up(message):
    Profile.objects.get_or_create(external_id = message.from_user.id)
    message = bot.send_message(message.from_user.id, "⬜⬜⬜⬜\nВведите Имя")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    profile, _ = Profile.objects.get_or_create(external_id = message.from_user.id)
    profile.name = message.text
    profile.save()
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_escape = types.KeyboardButton(text="Главное меню")
    keyboard.add(button_phone, button_escape)
    bot.send_message(message.from_user.id, "✅⬜⬜⬜\nОтправьте свой номер телефона (номер телефона необходимо отправить через клавиатуру снизу)", reply_markup=keyboard)


def get_descriptions(message):
    profile, _ = Profile.objects.get_or_create(external_id = message.from_user.id)
    profile.description = message.text
    profile.save()
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_location = types.KeyboardButton(text="Поделиться местоположением", request_location=True)
    keyboard.add(button_location, ck.main_menu_key)
    bot.send_message(message.from_user.id, "✅✅✅⬜\nДля завершения регистрации, отправьте свою гео локацию", reply_markup=keyboard)


@bot.message_handler(content_types=['contact', 'location'])
def contact(message):
    profile, _ = Profile.objects.get_or_create(external_id = message.from_user.id)
    if message.contact is not None:
        profile.phone = message.contact.phone_number
        profile.save()
        bot.send_message(message.from_user.id, "✅✅⬜⬜\nКоротко расскажите, чем Вы занимаетесь", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_descriptions)
    elif message.location is not None:
        profile.location_lat = message.location.latitude
        profile.location_lon = message.location.longitude
        profile.save()
        bot.send_message(message.from_user.id, "✅✅✅✅", reply_markup=ck.deleted_keyboard)
        bot.send_message(message.from_user.id, "Регистрация прошла успешно! Благодарим за использование нашего бота", reply_markup=ck.in_main_menu)


@logger.catch
def startUP_dating(message):
    startUP = StartUp_Profile.objects.all().exclude(viewed__isnull=True).order_by("?")
    print(startUP)
    if startUP.first():
        text = f"Стартап \"{startUP.first().name}\""
    else:
        text = 'Новых проектов еще не добавили, возможно хотите посмотреть старые?'

    bot.send_message(message.from_user.id, text)