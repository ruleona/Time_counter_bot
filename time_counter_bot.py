import telebot
from datetime import datetime, timedelta
from bot_token import TOKEN

bot = telebot.TeleBot(TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.start = None
        self.finish = None

@bot.message_handler(commands=["start"])
def greeting(message):
    chat_id = message.chat.id
    name = message.chat.first_name
    user = User(name)
    user_dict[chat_id] = user
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
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.start = start_time
        keyboard = telebot.types.ReplyKeyboardMarkup()
        finish_button = telebot.types.KeyboardButton("Конец работы")
        keyboard.row(finish_button)
        bot.send_message(message.chat.id, f"<b>Время начала:</b> \n\U0001F557{start_time_format}. \n\nХорошего дня!\U0001F31E", reply_markup=keyboard, parse_mode="html")
    elif message.text == "Конец работы":
        finish_time = datetime.now()
        finish_time_format = finish_time.strftime("%d.%m.%Y %H:%M")
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.finish = finish_time
        if timedelta(hours=8, minutes=45) > (finish_time - user.start):
            delta = timedelta(hours=8, minutes=45) - (finish_time - user.start)
            result_time = f"Недоработка: {delta.seconds // 60} мин."
        else:
            delta = (finish_time - user.start) - timedelta(hours=8, minutes=45)
            result_time = f"Переработка: {delta.seconds // 60} мин."
        keyboard = telebot.types.ReplyKeyboardMarkup()
        finish_button = telebot.types.KeyboardButton("Начало работы")
        keyboard.row(finish_button)
        bot.send_message(message.chat.id, f"<b>Время окончания:</b> \n\U0001F554{finish_time_format}. \n\n{result_time}\n\nПриятного отдыха!\U0001F31B", reply_markup=keyboard, parse_mode="html")
    else:
        bot.reply_to(message, "Сорри, я не знаю такой команды")

bot.polling(none_stop=True)
