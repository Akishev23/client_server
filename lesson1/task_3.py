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

start_words = ['attribute', 'класс', 'функция', 'type']

for word in start_words:
    try:
        word.encode('ascii')
    except UnicodeEncodeError as e:
        print(f'{word} - {using_bytes(word)}')



