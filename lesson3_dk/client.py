import socket
import sys
import threading
import logging

from useful.functions import listen_and_get, decode_and_send, say_hello, check_port
from useful.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS
from decor import logger, log

@log
def main_loop():
    if len(sys.argv) < 2:
        logger.info('Не указаны основные параметры запуска, применяю умолчания')
        server_adress, server_port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
    elif len(sys.argv) == 2:
        legger.info('Не указан порт, применяю умолчание')
        _, server_adress = sys.argv
        server_port = DEFAULT_PORT
    else:
        _, server_adress, server_port, *i = sys.argv
    if not check_port(server_port):
        logger.error(f'wrong port: {server_port}')
        sys.exit(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_adress, server_port))
    greeting = say_hello()
    # threading.Thread(target=decode_and_send, args=(sock, greeting)).start()
    decode_and_send(sock, greeting)
    listen_and_get(sock)


if __name__ == '__main__':
    main_loop()
