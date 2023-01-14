import json
import os

from loader import bot, markup


@bot.callback_query_handler(func=lambda c: True)
def get_choice(c):
    chat_id = c.message.chat.id
    if c.data == 'add_manga':
        msg = bot.send_message(chat_id, 'Введи название манги, за которой хочешь следить\n')
        bot.register_next_step_handler(msg, write_manga_names)
    elif c.data == 'manga_list':
        manga_names = sorted(get_manga_names(chat_id).items(), key=lambda dict_: int(dict_[0]))
        manga_names = ''.join([f'{k}. {v}\n' for k, v in manga_names])
        if manga_names:
            phrase = manga_names
        else:
            phrase = 'Добавленных манг пока нет'
        get_restart(chat_id, phrase=phrase)
    elif c.data == 'del_manga':
        manga_names = sorted(get_manga_names(chat_id).items(), key=lambda dict_: int(dict_[0]))
        manga_names = ''.join([f'{k}. {v}\n' for k, v in manga_names])
        if manga_names:
            bot.send_message(chat_id, manga_names)
            msg = bot.send_message(chat_id, 'Выбери номер манги, которую хочешь удалить')
            bot.register_next_step_handler(msg, del_manga)
        else:
            get_restart(chat_id, phrase='Добавленных манг пока нет')
    elif c.data == 'add_group':
        msg = bot.send_message(chat_id, 'Скопируй ссылку на группу вк')
        bot.register_next_step_handler(msg, write_group_list)
    elif c.data == 'group_list':
        group_names = sorted(get_group_names(chat_id).items(), key=lambda dict_: int(dict_[0]))
        group_names = ''.join([f'{k}. {v}\n' for k, v in group_names])
        if group_names:
            phrase = group_names
        else:
            phrase = 'Добавленных групп пока нет'
        get_restart(chat_id, phrase=phrase)
    elif c.data == 'del_group':
        group_names = sorted(get_group_names(chat_id).items(), key=lambda dict_: int(dict_[0]))
        group_names = ''.join([f'{k}. {v}\n' for k, v in group_names])
        if group_names:
            bot.send_message(chat_id, group_names)
            msg = bot.send_message(chat_id, 'Выбери номер группы, которую хочешь удалить')
            bot.register_next_step_handler(msg, del_group)
        else:
            get_restart(chat_id, phrase='Добавленных групп пока нет')
    elif c.data == 'cancel':
        get_restart(chat_id)


def get_restart(chat_id, phrase='Отмена'):
    bot.send_message(chat_id, phrase, reply_markup=markup)


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


def write_chat_ids(chat_id):
    if not os.path.exists('chat_ids.txt'):
        with open('chat_ids.txt', 'w') as file:
            file.write('')
    with open('chat_ids.txt') as file:
        chat_ids = [int(id_) for id_ in file.read().split('\n') if id_.isdigit()]
    if not chat_id in chat_ids:
        chat_ids.append(chat_id)
        with open('chat_ids.txt', 'w') as file:
            file.write('\n'.join([str(id_) for id_ in chat_ids]))
