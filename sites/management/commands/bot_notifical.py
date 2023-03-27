from django.db.models.signals import post_save
from django.dispatch import receiver


from loguru import logger
from telebot import types

from django.db.models import Q
from users.models import DatingCard_StartUp


from bot.management.commands import geo
from bot.management.commands import custom_keyboard as ck
from bot.management.commands.bot_connection import bot


@logger.catch
def start(message):
    user_id = message.from_user.id
    match_obj = DatingCard_StartUp.objects.filter(match_profile = True, match_start_up = True).filter(
        Q(start_up__ceo__external_id = user_id) |
        Q(card__profile__external_id = user_id)
        ).order_by("-match_start_up_datetime")[:10]
    logger.debug(match_obj)
    for item in match_obj:
        text = ""
        text += f"✅ {item.start_up.name}\n{item.start_up.idea}\n"
        text += f"💡 {item.start_up.ceo.name} @{item.start_up.ceo.username}\n"
        text += f"👤 {item.card.profile.name} @{item.card.profile.username}\n"
        
        x_A = str(item.start_up.ceo.location_lat).replace(',','.')
        y_A = str(item.start_up.ceo.location_lon).replace(',','.')
        x_B = str(item.card.profile.location_lat).replace(',','.')
        y_B = str(item.card.profile.location_lon).replace(',','.')

        text += f"Город: {geo.get_city(x_A, y_A)}\n"
        text += f"Расстояние: {geo.get_distance(x_A, y_A, x_B, y_B)}\n"
        bot.send_message(message.from_user.id, text)

    if not match_obj:
        text = 'Уведомлений еще нет'
        bot.send_message(message.from_user.id, text)


@logger.catch
@receiver(post_save, sender=DatingCard_StartUp)
def send_match(sender, instance, created, **kwargs):
    if instance.match_start_up and instance.match_profile:
        text_sctartUp = "Кто-то заинтересовался Вашим стартапом, проверьте уведомления"
        text_profile = "Кто-то заинтересовался Вашим профилем, проверьте уведомления"
        bot.send_message(instance.start_up.ceo.external_id, text=text_sctartUp)
        bot.send_message(instance.card.profile.external_id, text=text_profile)
    if instance.card.role == "I" and created:
        keyboard = types.InlineKeyboardMarkup()
        like_button = types.InlineKeyboardButton(text='Согласиться💚', callback_data=f'match_{instance.pk}')
        btn = types.InlineKeyboardButton(text=f"❌Отклонить", callback_data=f'escape')
        keyboard.add(like_button, btn)
        

        x_A = str(instance.card.profile.location_lat).replace(',', '.')
        y_A = str(instance.card.profile.location_lon).replace(',', '.')
        msg = f"❕Вашим стартапом заинтересовался инвестор:\n"
        msg += f"👤{instance.card.profile.name}\n"
        msg += f"💬{instance.card.profile.description}\n"
        msg += f"🏙 Город: {geo.get_city(x_A, y_A)[0]} , {geo.get_city(x_A, y_A)[1]}"
        bot.send_message(instance.start_up.ceo.external_id, text=msg, reply_markup=keyboard)
