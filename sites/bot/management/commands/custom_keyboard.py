
from django.conf import settings
from django.urls import reverse
from telebot import types

deleted_keyboard = types.ReplyKeyboardRemove()


# ОБЩИЕ КНОПКИ
signIn_key = types.InlineKeyboardButton(text='Вход', callback_data='signIn_key')
signOut_key = types.InlineKeyboardButton(text='Выход / Регистрация', callback_data='signOut_key')
registration_key = types.InlineKeyboardButton(text='Регистрация', callback_data='registration_key')
participate_key = types.InlineKeyboardButton(text='Участвовать ', callback_data='registration_key')

cancel_key = types.KeyboardButton(text='Отмена')

main_menu_key = types.KeyboardButton(text='Главное Меню')

clear_key = types.KeyboardButton(text='Очистить')
back_key = types.KeyboardButton(text='Назад')




respond_key = types.KeyboardButton(text='Откликнуться')
reveal_key = types.KeyboardButton(text='Раскрыть')

previous_key = types.KeyboardButton(text='Предыдущий')
next_key = types.KeyboardButton(text='Следующий')

connect_respond_key = types.KeyboardButton(text='Откликнуться')
next_startup_key = types.KeyboardButton(text='Следующий стартап')
deny_key = types.KeyboardButton(text='Отказать')

back_to_viewing_key = types.KeyboardButton(text='Вернуться к просмотру стартапа')
send_request_key = types.KeyboardButton(text='Отправить заявку')

mentor_key = types.KeyboardButton(text='Ментор')
expert_key = types.KeyboardButton(text='Эксперт')

feedback_key = types.InlineKeyboardButton(text='Отзывы', callback_data='feedback_key')
cases_key = types.InlineKeyboardButton(text='Кейсы', callback_data='cases_key')

# START FORM - KEYBOARD
start_keyboard = types.InlineKeyboardMarkup()

start_keyboard.add(registration_key, signIn_key)
start_keyboard.add(feedback_key, cases_key)

# INLINE BTN IN MAIN NAV
in_main_menu_btn = types.InlineKeyboardButton(text='Главное меню', callback_data='escape')
in_main_menu = types.InlineKeyboardMarkup()
in_main_menu.add(in_main_menu_btn)

def get_role_keyboard(user_role, startup_pk):
    keyboard = types.InlineKeyboardMarkup()
    for item in user_role.order_by('role'):
        descr = item.description
        if len(descr) > 10:
            descr = f": {descr[:10]}..."
        elif len(descr) > 0 and len(descr) <= 10:
            descr = f": {descr}"
        
        btn = types.InlineKeyboardButton(text=f"{item.get_role_display()}{descr}", callback_data=f'match_R_{item.pk}_{startup_pk}')
        keyboard.add(btn)
    btn = types.InlineKeyboardButton(text=f"⬅️ Назад", callback_data=f'escape')
    keyboard.add(btn)
    return keyboard

def get_startUp_keyboard(startUP, user_pk):
    keyboard = types.InlineKeyboardMarkup()
    for item in startUP:
        btn = types.InlineKeyboardButton(text=f"{item.name}", callback_data=f'match_C_{user_pk}_{item.pk}')
        keyboard.add(btn)
    btn = types.InlineKeyboardButton(text=f"⬅️ Назад", callback_data=f'escape')
    keyboard.add(btn)
    return keyboard


# КНОПКИ ДЛЯ МЕНЮ СТАТЬ ЭКСПЕРТОМ/МЕНТОРОМ/ИНВЕСТОРОМ
def create_role_keyboard(user_id):
    url = settings.BASE_URL + reverse("card_template", args=[user_id])[1:]
    webAppTest = types.WebAppInfo(url)
    keyboard = types.InlineKeyboardMarkup()
    create_expert_key_in = types.InlineKeyboardButton(text='Стать экспертом 🧐', web_app=webAppTest)
    create_mentor_key_in = types.InlineKeyboardButton(text='Стать ментором 👨‍🏫', web_app=webAppTest)
    create_invest_key_in = types.InlineKeyboardButton(text='Стать инвестором 💰', web_app=webAppTest)
    keyboard.add(create_expert_key_in, create_mentor_key_in)
    keyboard.add(create_invest_key_in)
    return keyboard

# BTN IN NAV MENU

def main_menu_keyboard(tg_id):
    url = settings.BASE_URL + reverse("add_startup", args=[tg_id])[1:]
    webAppTest = types.WebAppInfo(url)
    send_development = types.KeyboardButton(text='Написать в BizDate ⚙️')
    create_startup_key = types.KeyboardButton(text='Создать стартап 🎯', web_app=webAppTest)
    
    find_startup_key = types.KeyboardButton(text='Найти стартап 🔎')
    find_staff_key = types.KeyboardButton(text='Найти команду 🔎')
    notifications_key = types.KeyboardButton(text='Уведомления 🔔')
    favourites_key = types.KeyboardButton(text='Избранное ⭐')


    url = settings.BASE_URL + reverse("card_template", args=[tg_id])[1:]
    webAppTest = types.WebAppInfo(url)
    create_expert_key = types.KeyboardButton(text='Стать экспертом 🧐', web_app=webAppTest)
    create_mentor_key = types.KeyboardButton(text='Стать ментором 👨‍🏫', web_app=webAppTest)
    create_invest_key = types.KeyboardButton(text='Стать инвестором 💰', web_app=webAppTest)

    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    menu_keyboard.add(find_startup_key, find_staff_key)
    menu_keyboard.add(notifications_key, favourites_key)
    menu_keyboard.add(create_startup_key, create_expert_key, create_mentor_key, create_invest_key)
    menu_keyboard.add(send_development)
    return menu_keyboard

mesagge_form_keyboard = types.ReplyKeyboardMarkup()
mesagge_form_keyboard.add(connect_respond_key,deny_key)


connect_form_inline_keyboard = types.InlineKeyboardMarkup()
connect_form_inline_keyboard.add(respond_key,reveal_key)

