from loader import bot, HELP


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_message(message.chat.id, HELP)