import chardet

"""
Задание 6.

Создать  НЕ программно (вручную) текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».

Принудительно программно открыть файл в формате Unicode и вывести его содержимое.
Что это значит? Это значит, что при чтении файла вы должны явно указать кодировку utf-8
и файл должен открыться у ЛЮБОГО!!! человека при запуске вашего скрипта.

При сдаче задания в папке должен лежать текстовый файл!

Это значит вы должны предусмотреть случай, что вы по дефолту записали файл в cp1251,
а прочитать пытаетесь в utf-8.

Преподаватель будет запускать ваш скрипт и ошибок НЕ ДОЛЖНО появиться!

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО!!! в формате Unicode (utf-8)
--- обратите внимание на чтение файла в режиме rb
для последующей переконвертации в нужную кодировку

НАРУШЕНИЕ обозначенных условий - задание не выполнено!!!
"""
# Так как у меня файл сохраняется в utf, я его сначала конвертну в cp1251


def convert_to_utf8(file_p):
    with open(file_p, 'rb') as f:
        text = f.read()
        encoding = chardet.detect(text).get('encoding')
        if encoding != 'utf-8':
            text = text.decode(encoding)
            with open(file_p, 'wb') as file:
                file.write(text.encode('utf-8'))


def convert_to_cp1251(f_path):
    with open(f_path, 'rb') as f:
        text = f.read()
        encoding = chardet.detect(text).get('encoding')
        if encoding == 'utf-8':
            text = text.decode(encoding)
            with open(f_path, 'wb') as file:
                file.write(text.encode('cp1251'))


if __name__ == '__main__':

    file_path = 'test_file.txt'

    convert_to_cp1251(file_path)  # кодируем в cp1251 если кодировка отличается (по условию задачи)

    convert_to_utf8(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
