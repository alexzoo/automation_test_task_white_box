
# This code check what search service is available
# coding: utf-8
"""
 - Скрипт падает с ошибкой AssertionError. В итоге создается HTML тело, а не документ с ссылками - в данной реализации выкатывать нельзя.
 - Checkstyle - не соблюден:
    - Нет отступов
    - Импорты необходимо вынести на верх файла
    - Логирование необходимо переделать используя например библиотеку logging
    - Нечитабельный код, непонятно расположение методов. По-моему не хватает одного класса и структурированности.
 - Непонятные задвоенные значения в NEEDED_URLS, sleep -ы, import time, fetched_urls
"""

# Нет отступа от импортов, зачем 'https://yandex.ru/time/' задвоенна?
NEEDED_URLS = ['https://google.com/', 'https://www.semrush.com/', 'https://yandex.ru/time/', 'https://yandex.ru/time/']
# Добавить отступ
def get_fetch_urls(urls, cache={}):  # Нельзя применять мутабельные типы данных в методах
    import requests  # Переместить вверх файла
    urls_size = len(urls)
    result = []

    while urls_size:
        url = urls.pop()  # Изменяет коллекцию аргумент
        if url in cache:
            print('url in cache ' + url)
            result.append(cache[url])

        response = requests.get(url)
        body = response.content
        cache[url] = body
        result.append(body)  # Добавляет объект, а не ссылки
        urls_size -= 1

    return result
# Добавить 2 строки после получения результата
def get_full_moon_phase():  # Вместо отдельной функции лучше применить random сразу в UrlGetter
    import time  # Переместить вверх файла
    time.sleep(5)  # Не понятно зачем он нужен? Если нужен обьеденить со 2 слипом
    import random  # Переместить вверх файла
    time.sleep(5)  # Удалить или обьеденить с первым
    return random.choice([True, False])
# Добавить еще строку между классами
class UrlGetter:
    debug_mode_by_moon_phase = get_full_moon_phase()

    fetched_urls = []

    def __init__(self, fetched_urls):  # Переименовать переменную fetched_urls
        self.fetched_urls.extend(fetched_urls)

    def get_urls_data(self, urls):
        not_fetched_urls = []
        if self.debug_mode_by_moon_phase:
            for url in urls:  # Переименовать переменную url
                print(url)
        for url in urls:  # Переименовать переменную url, запутанные циклы надо их обьеденить или переписать
            if url not in self.fetched_urls:
                not_fetched_urls.append(url)
        data = get_fetch_urls(not_fetched_urls)
        self.fetched_urls.extend(not_fetched_urls)
        return data

    def check_url_not_fetched(self, url):  # Зачем этот метод? - лучше удалить
        if self.debug_mode_by_moon_phase:
            print(url in self.fetched_urls)
        return bool(url in self.fetched_urls)

# my tests
# Добавить отступ так как есть описание
fetched_urls = ['https://google.com/'] # Переменную убрать вверх класса
getter = UrlGetter(fetched_urls)
for url in NEEDED_URLS:
    print(getter.check_url_not_fetched(url))
reuzuult1 = getter.get_urls_data(NEEDED_URLS)   # reuzuult1 - Нечитаемое имя переменной

import time  # Переместить вверх файла, о выше уже есть один - просто удаляем
time.sleep(5)  # Не понятно зачем он нужен?

fetched_urls = ['https://google.com/']  # Задвоенная переменная fetched_urls  - удалить
getter = UrlGetter(NEEDED_URLS)
reuzuult2 = getter.get_urls_data(NEEDED_URLS)  # reuzuult2 - Нечитаемое имя переменной


import os  # Переместить вверх файла
file = open(os.getcwd()+'/data1.html', 'wb')
file.writelines(reuzuult1)  # Файл остается не закрытым
file2 = open(os.getcwd()+'/data2.html', 'wb')
file2.writelines(reuzuult2)  # Файл остается не закрытым

assert reuzuult1 == reuzuult2

if __name__ == '__main__':
    getter = UrlGetter()  # Нет аргумента.
    print(getter.get_urls_data(NEEDED_URLS))
# Нет пустой строки в конце файла