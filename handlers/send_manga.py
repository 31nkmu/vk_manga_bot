from loader import bot, markup, CHOICE
from services import get_choice, get_manga_names, get_group_names
from vk_parser import get_parser_data


@bot.message_handler(commands=['send_manga'])
def send_manga(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Подожди, идет поиск глав')
    group_list = [group_name for group_name in get_group_names().values()]
    manga_list = [manga for manga in get_manga_names().values()]
    parser_data = get_parser_data(group_list=group_list, manga_list=manga_list)
    if parser_data:
        for data in parser_data:
            bot.send_message(chat_id, data)
    else:
        bot.send_message(chat_id, 'Новых глав пока нет')
    msg = bot.send_message(chat_id, CHOICE, reply_markup=markup)
    bot.register_next_step_handler(msg, get_choice)
    # send_manga(message)


