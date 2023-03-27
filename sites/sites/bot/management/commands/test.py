
# @bot.message_handler(commands=['test'])
# def start_message(message):
    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
    # markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
    # markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
    # bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id,f'Приветствую {message.from_user.first_name}')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Войти")
    item2=types.KeyboardButton("Регистрация")
    markup.add(item1,item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_from_user(message):
    if message.text.lower() == 'войти':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Вход")
        item2=types.KeyboardButton("Отмена")
        markup.add(item1,item2)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    elif message.text.lower() == 'регистрация':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Зарегистрироваться ")
        item2=types.KeyboardButton("Отмена")
        markup.add(item1,item2)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    elif message.text.lower() == 'вход':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Действия")
        item2=types.KeyboardButton("Уведомления")
        item3=types.KeyboardButton("Избранное")
        item4=types.KeyboardButton("главное меню")
        markup.add(item1,item2,item3)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    elif message.text.lower() == 'действия':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("действие 1")
        item2=types.KeyboardButton("действие 2")
        item3=types.KeyboardButton("действие 3")
        item4=types.KeyboardButton("главное меню")
        markup.add(item1,item2,item3,item4)
        bot.send_message(message.chat.id,'Выберите действие',reply_markup=markup)
    elif message.text.lower() == 'уведомления':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("главное меню")
        markup.add(item1)
        bot.send_message(message.chat.id,'Выберите действие',reply_markup=markup)
        # markup.add(item1,item2,item3)
        bot.send_message(message.chat.id,'Ваши уведомления') 
    elif message.text.lower() == 'избранное':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        # item1=types.KeyboardButton("действие 1")
        # item2=types.KeyboardButton("действие 2")
        # item3=types.KeyboardButton("действие 3")
        # markup.add(item1,item2,item3)
        bot.send_message(message.chat.id,'Ваше избранное')   
    elif message.text.lower() == 'главное меню':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Действия")
        item2=types.KeyboardButton("Уведомления")
        item3=types.KeyboardButton("Избранное")
        markup.add(item1,item2,item3)
        bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
    answer = ''
    if call.data == 'login':
        answer = 'Вы троечник!'
    elif call.data == 'registration':
        answer = 'Вы хорошист!'

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.infinity_polling(none_stop=True)