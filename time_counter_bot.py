import telebot
from datetime import datetime, timedelta
from token import bot_token

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=["start"])
def greeting(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    start_button = telebot.types.KeyboardButton("Начало работы")
    keyboard.row(start_button)
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}. Я помогу тебе посчитать рабочее время. Нажми кнопку <b>\"Начало\"</b>, когда придешь на работу", parse_mode="html", reply_markup=keyboard)

@bot.message_handler(content_types=["photo"])
def get_content(message):
    bot.reply_to(message, "Отличное фото!")

@bot.message_handler()
def answer(message):
    if message.text == "Начало работы":
        start_time = datetime.now()
        start_time_format = start_time.strftime("%d.%m.%Y %H:%M")
        global check_time
        check_time = start_time
        keyboard = telebot.types.ReplyKeyboardMarkup()
        finish_button = telebot.types.KeyboardButton("Конец работы")
        keyboard.row(finish_button)
        bot.send_message(message.chat.id, f"<b>Время начала:</b> \n\U0001F557{start_time_format}. \n\nХорошего дня!\U0001F31E", reply_markup=keyboard, parse_mode="html")
    elif message.text == "Конец работы":
        finish_time = datetime.now()
        finish_time_format = finish_time.strftime("%d.%m.%Y %H:%M")
        global check_time
        if timedelta(hours=8, minutes=45) > (finish_time - check_time):
            delta = timedelta(hours=8, minutes=45) - (finish_time - check_time)
            result_time = f"Недоработка: {delta.seconds / 60}"
        else:
            delta = (finish_time - check_time) - timedelta(hours=8, minutes=45)
            result_time = f"Переработка: {delta.seconds / 60}"
        keyboard = telebot.types.ReplyKeyboardMarkup()
        finish_button = telebot.types.KeyboardButton("Начало работы")
        keyboard.row(finish_button)
        bot.send_message(message.chat.id, f"<b>Время окончания:</b> \n\U0001F554{finish_time_format}. \n\nПриятного отдыха!\U0001F31B", reply_markup=keyboard, parse_mode="html")
    else:
        bot.reply_to(message, "Сорри, я не знаю такой команды")

bot.polling(none_stop=True)