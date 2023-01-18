import json
import os

import requests
from decouple import config
from bs4 import BeautifulSoup as Bs

new_chapters = dict()


def get_wall_chapters(group_name, favorite_chapters, chat_id):
    global new_chapters
    src = get_src(group_name=group_name)
    make_dir(group_name=group_name)
    write_json(group_name=group_name, src=src)
    chapters = src['response']['items']

    # проверяем есть ли файл с ID. если есть делаем проверку и отправляем только новые посты, иначе просто создаем.
    if not os.path.exists(f'{group_name}/exist_chapter_{group_name}_{chat_id}.json'):
        old_chapters_id = dict()
    else:
        with open(f'{group_name}/exist_chapter_{group_name}_{chat_id}.json') as file:
            old_chapters_id = json.load(file)
    res = []
    for old_chapter in old_chapters_id:
        for ind, favorite_chapter in enumerate(favorite_chapters):
            if favorite_chapter in old_chapter.lower():
                favorite_chapters[ind] = old_chapter.lower()
    for favorite_chapter in favorite_chapters:
        old_chapter_id = None
        for chapter, id_ in old_chapters_id.items():
            if favorite_chapter.strip() in chapter:
                old_chapter_id = id_
                break
        link = get_fresh_chapters(chapters=chapters, old_chapter_id=old_chapter_id, favorite_chapter=favorite_chapter)
        if link:
            res.append(link)
    old_chapters_id.update(new_chapters)

    with open(f'{group_name}/exist_chapter_{group_name}_{chat_id}.json', 'w', encoding='utf-8') as file:
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
        pass
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


def get_fresh_chapters(chapters: list, old_chapter_id: int,
                       favorite_chapter: str):
    """
    находит ссылки новых доступных избранных глав манг
    :param chapters: все главы
    :param old_chapter_id: id старой главы
    :param favorite_chapter: названия избранной главы
    :return: ссылка на главу
    """
    for chapter in chapters:
        chapter_id = chapter['id']
        try:
            if chapter_id == old_chapter_id:
                return None
            if chapter['attachments']:
                attachments = chapter['attachments']
            else:
                attachments = chapter['copy_history'][0]['attachments']
            if favorite_chapter.lower().replace('ё', 'е') in chapter['text'].lower().replace('ё', 'е'):
                for attachment in attachments:
                    if attachment.get('type') == 'link':
                        url = attachment['link']['url']
                        if check_chapter_access(url=url):
                            title = attachment['link']['title'].split(' ')
                            title = ' '.join(
                                [word.lower().strip('-').strip() for word in title if any(i in ',:;./\\+=-!?' or i.isalpha() for i in word)
                                 and not 'глав' in word.lower()]).replace('ё', 'е')
                            new_chapters.update({title: chapter_id})
                            return url
        except Exception as ex_:
            continue


def get_parser_data(chat_id):
    with open(f'groups/{chat_id}.json') as file:
        group_list = json.load(file)
    group_list = [group for group in group_list.values()]
    with open(f'manga_names/{chat_id}.json') as file:
        manga_names = json.load(file)
    manga_list = [manga for manga in manga_names.values()]
    data = []
    for group_name in group_list:
        for one_data in get_wall_chapters(group_name=group_name, favorite_chapters=manga_list, chat_id=chat_id):
            data.append(one_data)
    return data


if __name__ == '__main__':
    print('RES', get_parser_data('144400282'))
