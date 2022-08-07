import csv
from glob import glob
import chardet

"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

# Не понял, индексы 1, 2, 3 - обязательное требование? если да, я добавлю


def get_data(template):
    list_of_files = [glob(f'{template}*')][0]
    global_list = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    for file_path in list_of_files:
        with open(file_path, 'rb') as f:
            file = f.read()
            enc = chardet.detect(file).get('encoding')
        with open(file_path, 'r', encoding=enc) as f:
            data = csv.reader(f, skipinitialspace=True, delimiter=':')
            sp = {}
            for line in data:
                try:
                    name, value, *tail = line
                    if name in global_list[0]:
                        sp[global_list[0].index(name)] = value
                except ValueError:
                    pass
            global_list.append([sp_sorted[1] for sp_sorted in sorted(sp.items())])

    return global_list


def write_to_csv(file, template):
    with open(file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        data_to_write = get_data(template)
        writer.writerows(data_to_write)


if __name__ == '__main__':
    template = 'info_'
    write_to_csv('common.csv', template)
