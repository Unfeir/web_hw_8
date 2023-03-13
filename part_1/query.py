from model import Authors, Quotes

from colorama import Fore, Style
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

"""Pеалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів.
Скрипт виконується в нескінченному циклі
і за допомогою звичайного оператора input приймає команди
у наступному форматі команда: значення.
Приклад:
    name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
    tag:life — знайти та повернути список цитат для тега life;
    tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
    exit — завершити виконання скрипту;
Виведення результатів пошуку лише у форматі utf-8;"""


def build_response(quotes):
    """build string presentment for quotes in DB"""
    quote_to_print = ""
    for el in quotes:
        quote_to_print += f"\n{Fore.BLUE}{el.author.fullname}{Style.RESET_ALL}\n"
        quote_to_print += f"{Fore.GREEN}{el.tags}{Style.RESET_ALL}\n"
        quote_to_print += f"{Fore.GREEN}{el.quote}{Style.RESET_ALL}\n"
        quote_to_print += "-" * 50
    return quote_to_print

@cache
def authors_quotes(name):
    """function search quotes by author.
    If no Author - call function to search with not a strict match"""
    author = Authors.objects(fullname=name)
    if author:
        for el in author:
            qouts = Quotes.objects(author=el.id)
            return build_response(qouts)

    return istartswith_author(name)

@cache
def istartswith_author(name):
    """Search by first letters of Author name"""
    author = Authors.objects(fullname__istartswith=name)
    if author:
        for el in author:
            qouts = Quotes.objects(author=el.id)
            return build_response(qouts)

    return f"{name} have no quotes"

@cache
def search_tags(tags):
    """function search quotes by tags.
        If no quotes - call function to search with not a strict match"""
    result = []
    for tag in tags:
        quot = Quotes.objects(tags=tag)
        if quot:
            result.extend(quot)

    if result:
        return build_response(result)
    else:
        return istartswith_tags(tags)

@cache
def istartswith_tags(tags):
    """function search quotes by tags.
        If no quotes - call function to search with not a strict match"""
    result = []
    for tag in tags:
        quot = Quotes.objects(tags__istartswith=tag)
        if quot:
            result.extend(quot)

    if result:
        return build_response(result)
    else:
        return 'No quotes with surch tags'


def query():
    while True:
        hlp = "type name or tag and argument separatede by ':' \nexample: name:Albert Einstein \nor exit"
        user_input = input("Input tag or name for search: ")
        splited = user_input.split(":")
        command = splited[:1]

        args = []
        if len(splited) > 1:
            args = splited[1:][0].split(",")
        match command[0]:
            case "name":
                for name in args:
                    print(authors_quotes(name))
            case "tag" | "tags":
                print(search_tags(args))
            case "exit":
                exit()
            case _:
                print(hlp)


if __name__ == '__main__':
    query()

