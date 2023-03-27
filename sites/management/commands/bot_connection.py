from django.conf import settings

import telebot


bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)