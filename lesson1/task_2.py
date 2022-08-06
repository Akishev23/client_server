import sys
"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""
# В задаче сказано испольщовать b'' - запись, но я усложнил, чтобы избежать исключений для не
# ascii- символов. кстати, методы дают слегка разные результаты

start_words = ['class', 'function', 'method']
start_bytes = {b'class', b'function', b'method'}


def using_bytes(string):
    return bytes(string, encoding='utf-8')


def using_b(string):
    return b'%a' % string


if __name__ == '__main__':
    for word in start_words:
        print(f'{type(word)} - {len(word)} символов - {word}')
        print(f'{type(using_bytes(word))} - {sys.getsizeof(using_bytes(word))} байт -'
              f' {using_bytes(word)}')
        print(f'{type(using_b(word))} - {sys.getsizeof(using_b(word))} байт -'
              f' {using_b(word)}')

    for bytes in start_bytes:
        print(f'{type(bytes)} - {len(bytes)} символов - {bytes}')
