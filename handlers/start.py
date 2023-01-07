from loader import bot, CHOICE, markup
from services import get_choice


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет, я бот, который может отправлять тебе свежие главы твоих любимых манг')
    msg = bot.send_message(chat_id, CHOICE, reply_markup=markup)
    bot.register_next_step_handler(msg, get_choice)
