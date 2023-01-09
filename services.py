import json
import os

from loader import bot, CHOICE, markup
from vk_parser import get_parser_data


def get_choice(message):
    chat_id = message.chat.id
    if message.text == '1':
        msg = bot.send_message(chat_id, 'Введи название манги, за которой хочешь следить\n')
        bot.register_next_step_handler(msg, write_manga_names)
    elif message.text == '2':
        msg = bot.send_message(chat_id, 'Скопируй ссылку на группу вк')
        bot.register_next_step_handler(msg, write_group_list)
    elif message.text == '3':
        manga_names = ''.join([f'{k}. {v}\n' for k, v in sorted(get_manga_names(chat_id).items())])
        if manga_names:
            phrase = manga_names
        else:
            phrase = 'Добавленных манг пока нет'
        get_restart(chat_id, phrase=phrase)
    elif message.text == '4':
        group_names = ''.join([f'{k}. {v}\n' for k, v in sorted(get_group_names(chat_id).items())])
        if group_names:
            phrase = group_names
        else:
            phrase = 'Добавленных групп пока нет'
        get_restart(chat_id, phrase=phrase)
    elif message.text == '5':
        group_names = ''.join([f'{k}. {v}\n' for k, v in sorted(get_group_names(chat_id).items())])
        if group_names:
            bot.send_message(chat_id, group_names)
            msg = bot.send_message(chat_id, 'Выбери номер группы, которую хочешь удалить')
            bot.register_next_step_handler(msg, del_group)
        else:
            get_restart(chat_id, phrase='Добавленных групп пока нет')
    elif message.text == '6':
        manga_names = ''.join([f'{k}. {v}\n' for k, v in sorted(get_manga_names(chat_id).items())])
        if manga_names:
            bot.send_message(chat_id, manga_names)
            msg = bot.send_message(chat_id, 'Выбери номер манги, которую хочешь удалить')
            bot.register_next_step_handler(msg, del_manga)
        else:
            get_restart(chat_id, phrase='Добавленных манг пока нет')
    elif message.text == '/restart':
        get_restart(chat_id)
    elif message.text == '/send_manga':
        send_manga(chat_id)


def get_restart(chat_id, phrase='Перезапускаем бота'):
    bot.send_message(chat_id, phrase)
    msg = bot.send_message(chat_id, CHOICE, reply_markup=markup)
    bot.register_next_step_handler(msg, get_choice)


def write_manga_names(message):
    chat_id = message.chat.id
    if message.text == '/restart':
        get_restart(chat_id)
    else:
        manga_names = get_manga_names(chat_id)
        id_ = len(manga_names) + 1
        if str(id_) in manga_names:
            for i in range(1, id_):
                if not str(i) in manga_names:
                    id_ = i
                    break
        manga_names.update({id_: message.text.lower()})
        if not os.path.exists('manga_names'):
            os.mkdir('manga_names')
        with open(f'manga_names/{chat_id}.json', 'w') as file:
            json.dump(manga_names, file, ensure_ascii=False, indent=4)
        get_restart(chat_id, phrase=f'Манга "{message.text}" добавлена')


def write_group_list(message):
    chat_id = message.chat.id
    if message.text == '/restart':
        get_restart(chat_id)
    else:
        group_names = get_group_names(chat_id)
        id_ = len(group_names) + 1
        if str(id_) in group_names:
            for i in range(1, id_):
                if not str(i) in group_names:
                    id_ = i
                    break
        group_names.update({id_: message.text.split('/')[-1]})
        if not os.path.exists('groups'):
            os.mkdir('groups')
        with open(f'groups/{chat_id}.json', 'w') as file:
            json.dump(group_names, file, ensure_ascii=False, indent=4)
        get_restart(chat_id, phrase=f"Группа {message.text.split('/')[-1]} добавлена")


def get_group_names(chat_id):
    if os.path.exists(f'groups/{chat_id}.json'):
        with open(f'groups/{chat_id}.json') as file:
            return json.load(file)
    else:
        return {}


def get_manga_names(chat_id):
    if os.path.exists(f'manga_names/{chat_id}.json'):
        with open(f'manga_names/{chat_id}.json') as file:
            return json.load(file)
    else:
        return {}


def del_group(message):
    chat_id = message.chat.id
    if message.text == '/restart':
        get_restart(chat_id)
    else:
        group_names = get_group_names(chat_id)
        if group_names.get(message.text):
            group_names.pop(message.text, None)
            with open(f'groups/{chat_id}.json', 'w') as file:
                json.dump(group_names, file, ensure_ascii=False, indent=4)
            phrase = f'Группа под номером {message.text} удалена'
            get_restart(chat_id, phrase=phrase)
        else:
            phrase = 'Неправильный номер группы, выбери снова'
            msg = bot.send_message(chat_id, phrase)
            bot.register_next_step_handler(msg, del_group)


def del_manga(message):
    chat_id = message.chat.id
    if message.text == '/restart':
        get_restart(chat_id)
    else:
        manga_names = get_manga_names(chat_id)
        if manga_names.get(message.text):
            manga_names.pop(message.text, None)
            with open(f'manga_names/{chat_id}.json', 'w') as file:
                json.dump(manga_names, file, ensure_ascii=False, indent=4)
            phrase = f'Манга под номером {message.text} удалена'
            get_restart(chat_id, phrase=phrase)
        else:
            phrase = 'Неправильный номер манги, выбери снова'
            msg = bot.send_message(chat_id, phrase)
            bot.register_next_step_handler(msg, del_manga)


def send_manga(chat_id):
    bot.send_message(chat_id, 'Подожди, идет поиск глав')
    parser_data = get_parser_data(chat_id)
    if parser_data:
        for data in parser_data:
            bot.send_message(chat_id, data)
    else:
        bot.send_message(chat_id, 'Новых глав пока нет')
    msg = bot.send_message(chat_id, CHOICE, reply_markup=markup)
    bot.register_next_step_handler(msg, get_choice)


def write_chat_ids(chat_id):
    if not os.path.exists('chat_ids.txt'):
        with open('chat_ids.txt', 'w') as file:
            file.write('')
    with open('chat_ids.txt') as file:
        chat_ids = [int(id_) for id_ in file.read.split('\n')]
    if not chat_id in chat_ids:
        chat_ids.append(chat_id)
        with open('chat_ids.txt', 'w') as file:
            file.write('\n'.join([str(id_) for id_ in chat_ids]))
