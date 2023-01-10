from threading import Thread
import time

from loader import bot
from vk_parser import get_parser_data

with open('chat_ids.txt') as file:
    chat_id = file.read()

CHAT_ID = chat_id.split('\n')


def send_manga_async(bot):
    while True:
        for id_ in CHAT_ID:
            try:
                parser_data = get_parser_data(id_)
                if parser_data:
                    for data in parser_data:
                        bot.send_message(id_, data)
            except:
                continue
        time.sleep(10)


# Создаем новый поток и в нем запускаем нашу функцию:
Thread(target=send_manga_async, args=(bot,)).start()
