import json
import os

import requests
from decouple import config
from bs4 import BeautifulSoup as Bs

new_chapters = dict()


def get_wall_chapters(group_name, favorite_chapters):
    global new_chapters
    src = get_src(group_name=group_name)
    make_dir(group_name=group_name)
    write_json(group_name=group_name, src=src)
    chapters = src['response']['items']

    # проверяем есть ли файл с ID. если есть делаем проверку и отправляем только новые посты, иначе просто создаем.
    if not os.path.exists(f'{group_name}/exist_chapter_{group_name}.json'):
        print('файла с ID глав не существует, создаем файл...')

        old_chapters_id = dict()
        with open(f'{group_name}/exist_chapter_{group_name}.json', 'w', encoding='utf-8') as file:
            json.dump(dict(), file, indent=4, ensure_ascii=False)

    else:
        print('файл с ID глав уже существует, начинаем выборку свежих глав...')
        with open(f'{group_name}/exist_chapter_{group_name}.json') as file:
            old_chapters_id = json.load(file)

    res = []
    for old_chapter in old_chapters_id:
        for ind, favorite_chapter in enumerate(favorite_chapters):
            if favorite_chapter in old_chapter.lower():
                favorite_chapters[ind] = old_chapter.lower()
    for favorite_chapter in favorite_chapters:
        link = get_fresh_chapters(chapters=chapters, old_chapters_id=old_chapters_id, favorite_chapter=favorite_chapter)
        if link:
            res.append(link)
    if new_chapters:
        old_chapters_id.update(new_chapters)

        with open(f'{group_name}/exist_chapter_{group_name}.json', 'w', encoding='utf-8') as file:
            json.dump(old_chapters_id, file, indent=4, ensure_ascii=False)
    new_chapters = dict()
    return res


def check_chapter_access(url: str) -> bool:
    """
    Проверяет доступна ли глава без доната
    :param url: ссылка на главу
    """
    response = requests.get(url)
    soup = Bs(response.text, 'lxml')
    catalog = soup.find('div', class_='ArticleDonut__title')
    return not bool(catalog)


def get_src(group_name):
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={config("token")}&v=5.131'
    req = requests.get(url)
    return req.json()


def make_dir(group_name):
    """
    проверяем существует ли директория с таким именем
    :param group_name: имя директории
    """
    if os.path.exists(f'{group_name}'):
        print(f'директория с именем {group_name} существует')
    else:
        os.mkdir(group_name)


def write_json(group_name, src):
    """
    сохраним данные в json файл
    :param group_name: имя файла
    :param src: данные, которые нужно записать
    """
    with open(f'{group_name}/{group_name}.json', 'w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)


def get_fresh_chapters(chapters: list, old_chapters_id: str or list,
                       favorite_chapter: str):
    """
    находит ссылки новых доступных избранных глав манг
    :param chapters: все главы
    :param old_chapters_id: список старых глав
    :param favorite_chapter: названия избранной главы
    :return: ссылка на главу
    """
    for chapter in chapters:
        chapter_id = chapter['id']
        print(f'отправляем главу с ID {chapter_id}')
        try:
            if chapter_id == old_chapters_id.get(favorite_chapter, False):
                return None
            if chapter['attachments']:
                attachments = chapter['attachments']
            else:
                attachments = chapter['copy_history'][0]['attachments']
            for attachment in attachments:
                if attachment.get('type') == 'link' and favorite_chapter.lower():
                    if favorite_chapter.lower().replace('ё', 'е') in attachment['link']['title'].lower().replace('ё',
                                                                                                                 'е'):
                        url = attachment['link']['url']
                        if check_chapter_access(url=url):
                            title = attachment['link']['title'].split(' ')
                            title = ' '.join(
                                [word.lower() for word in title if
                                 word.isalpha() and not 'глав' in word.lower()]).replace('ё', 'е')
                            new_chapters.update({title: chapter_id})
                            return url
        except Exception:
            print(f'что-то пошло не так с главой под ID {chapter_id}')


def get_parser_data(group_list, manga_list):
    data = []
    for group_name in group_list:
        for one_data in get_wall_chapters(group_name=group_name, favorite_chapters=manga_list):
            data.append(one_data)
    return data


# if __name__ == '__main__':
#     from services import get_manga_names, get_group_names
#
#     group_list = [group for group in get_group_names().values()]
#     manga_names = [manga for manga in get_manga_names().values()]
#     print('GROUP_LIST', group_list)
#     print('MANGA_NAMES', manga_names)
#     res = get_parser_data(group_list=group_list,
#                           manga_list=manga_names)
#     print(res)
