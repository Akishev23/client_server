from task_2 import using_bytes

"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""
# в байтовой записи не может быть символов, не относящихся к ASCII

# Замечание преподавателя "нет отлова исключения без encode decode". Я проглядел это задание

start_words = ['attribute', 'класс', 'функция', 'type']

for word in start_words:
    try:
        word.encode('ascii')
    except UnicodeEncodeError:
        print(f'{word} - {using_bytes(word)}')


for word in start_words:
    try:
        bytes(word, 'ascii')
    except UnicodeEncodeError:
        print(f'Слово {word} нельзя записать с помощью b""')
        # print(f'{word} - {using_bytes(word)}')
        print(b'%a' % word)
