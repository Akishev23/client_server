import subprocess
import chardet

"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

res = subprocess.Popen(['ping', 'yandex.ru'], stdout=subprocess.PIPE)

output = res.communicate()

for i in output:
    if i:
        encoding = chardet.detect(i).get('encoding')
        line = i.decode(encoding).encode('utf-8')
        print(line.decode('utf-8'))
