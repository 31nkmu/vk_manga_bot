import telebot
from decouple import config
from telebot import types

bot = telebot.TeleBot(config('bot_token'))

markup = types.InlineKeyboardMarkup(row_width=2)
b1 = types.InlineKeyboardButton('Доб мангу', callback_data='add_manga')
b2 = types.InlineKeyboardButton('Список манг', callback_data='manga_list')
b3 = types.InlineKeyboardButton('Удалить мангу', callback_data='del_manga')
b4 = types.InlineKeyboardButton('Доб группу', callback_data='add_group')
b5 = types.InlineKeyboardButton('Список групп', callback_data='group_list')
b6 = types.InlineKeyboardButton('Удалить группу', callback_data='del_group')
b7 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
markup.add(b1, b4, b3, b6, b2, b5, b7)
