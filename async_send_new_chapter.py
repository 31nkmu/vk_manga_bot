from threading import Thread
import time

from loader import bot
from vk_parser import get_parser_data


def send_manga_async(bot):
    while True:
        try:
            with open('chat_ids.txt') as file:
                chat_id = file.read()
        except FileNotFoundError:
            chat_id = ''
        chat_ids = chat_id.split('\n')

        for id_ in chat_ids:
            try:
                parser_data = get_parser_data(id_)
                if parser_data:
                    for data in parser_data:
                        bot.send_message(id_, data)
            except Exception as ex_:
                print(ex_)
        time.sleep(10)


# Создаем новый поток и в нем запускаем нашу функцию:
Thread(target=send_manga_async, args=(bot,)).start()
