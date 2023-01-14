from loader import bot, markup
from services import get_choice, write_chat_ids


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    write_chat_ids(chat_id)
    bot.send_message(chat_id,
                     'Привет, я бот, который будет автоматически отправлять тебе свежие главы твоих любимых манг',
                     reply_markup=markup)
