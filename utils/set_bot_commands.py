from telebot import types

from loader import bot

bot.set_my_commands([
    types.BotCommand('/start', 'Запуск бота'),
    types.BotCommand('/restart', 'Перезапуск бота'),
    types.BotCommand('/send_manga', 'Отправить свежие главы'),
    types.BotCommand('/help', 'Помощь'),
])
