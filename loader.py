import telebot
from decouple import config
from telebot import types

bot = telebot.TeleBot(config('bot_token'))

CHOICE = '1. Выбрать(добавить) мангу, свежие главы которой хочешь получать\n' \
         '2. Выбрать(добавить) группу вконтакте, в которой будут следить за новыми главами\n' \
         '3. Показать список манг, за которыми ты уже следишь\n' \
         '4. Показать список групп вконтакте\n' \
         '5. Удалить группу вк\n' \
         '6. Удалить мангу'

HELP = 'если хочешь отменить действие, перезапусти бота: /restart\n' \
       'отправка свежих глав: /send_manga\n' \
       'все варианты команд есть у тебя в меню'

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=6)
b1 = types.KeyboardButton('1')
b2 = types.KeyboardButton('2')
b3 = types.KeyboardButton('3')
b4 = types.KeyboardButton('4')
b5 = types.KeyboardButton('5')
b6 = types.KeyboardButton('6')
markup.add(b1, b2, b3, b4, b5, b6)
