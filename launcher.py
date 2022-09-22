"""
launcher for convenience to test
"""
# -*- coding: utf-8 -*-
import subprocess

processes = []

while True:
    param = input('Choose the command: q - quit, '
                  's + n  - launch server and n clients, x - close all the windows: ')

    if 'q' in param:
        break
    if 's' in param:
        n = int(param.strip('s'))
        processes.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(n):
            processes.append(subprocess.Popen('python client.py -m send',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(n):
            processes.append(subprocess.Popen('python client.py -m listen',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif param == 'x':
        while processes:
            p_to_del = processes.pop()
            p_to_del.kill()
