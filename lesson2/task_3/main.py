import yaml

"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""


def write_to_yaml(file, data):
    with open(file, 'w') as f:
        yaml.dump(all_data, f, allow_unicode=True, default_flow_style=False)
    return 0


def read_from_yaml(file):
    with open(file, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


if __name__ == '__main__':
    items = ['computer', 'printer', 'mouse', 'keyboard']

    items_quantity = 10

    items_ptices = {
        'computer': '5000€',
        'printer': '500£',
        'mouse': '1¥ - ∞',
        'keyboard': '≈100₽'
    }

    all_data = {
        'items': items,
        'items_quantity': items_quantity,
        'items_ptice': items_ptices
    }

    write_to_yaml('stock.yaml', all_data)
    print(read_from_yaml('stock.yaml'))
