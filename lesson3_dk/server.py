import socket
import threading
import logging
import sys
import os
from json import JSONDecodeError
from variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, \
    USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from functions import check_port, listen_and_get, decode_and_send, decode_message
from decor import logger, log



sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


@log
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'guest':
        logger.debug(f'got correct message from client {message}')
        return {RESPONSE: 200}
    logger.error('gof incorrect message from client {message}')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

@log
def accept_client(sock):
    while True:
        client, address = sock.accept()
        logger.info(f'Client with address {address} connected')
        return client, address

@log
def main_server():
    listen_port = DEFAULT_PORT
    listen_address = DEFAULT_IP_ADDRESS

    for index, name in enumerate(sys.argv):
        next_i = index + 1
        if name == '-p' and len(sys.argv) >= next_i + 1:
            listen_port = sys.argv[next_i]
        if name == '-a' and len(sys.argv) >= next_i + 1:
            listen_address = sys.argv[next_i]

    if not check_port(listen_port):
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_address, listen_port))
    sock.listen(MAX_CONNECTIONS)
    client = accept_client(sock)[0]

    while True:
        message_from_client = listen_and_get(client)
        if message_from_client:
            logger.info(f'got message from client: {message_from_client}')
            resp = process_client_message(message_from_client)
            logger.info(f'here is a processed message {resp}')
            try:
                decode_and_send(client, resp)
            except (ValueError, JSONDecodeError):
                logger.exception('Invalid client message format, below is the info')
                client.close()


if __name__ == '__main__':
    main_server()

