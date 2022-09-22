"""
server part of the project
"""
# -*- coding: utf-8 -*-
import socket
import select
import time
from libr.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, \
    USER, ERROR, MESSAGE_TEXT, MESSAGE, SENDER
from libr.functions import listen_and_get, decode_and_send, args_parser
from decor import logger, log


@log
def process_client_message(message, messages, client):
    """
    processing client's message
    :param messages: list
    :param client: socket object
    :param message: dictionary
    :return: empty
    """
    presence_keys = [ACTION, TIME, USER]
    message_keys = [ACTION, TIME, ACCOUNT_NAME, MESSAGE_TEXT]

    if all(message.get(key) for key in presence_keys) and message[ACTION] == PRESENCE:
        logger.debug(f'got correct message of presence from client {message}')
        decode_and_send(client, {RESPONSE: 200})
        return

    if all(message.get(key) for key in message_keys) and message[ACTION] == MESSAGE:
        messages.append([message[ACCOUNT_NAME], message[MESSAGE_TEXT]])
        logger.debug(f'got correct message from client {message}')
        return

    logger.error(f'got incorrect message from client {message}')
    bad_req = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    decode_and_send(client, bad_req)
    return


@log
def accept_client(sock):
    """
    accepting clients
    :param sock: socket object
    :return: cortege of socket object and client ip
    """
    while True:
        client, address = sock.accept()
        logger.info(f'Client with address {address} connected')
        return client, address


@log
def main_server():
    """
    main function of server's part
    :return:
    """

    listen_address, listen_port = args_parser()

    logger.info(f'Запускаю сервер с параметрами port = {listen_port}, address = {listen_address}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_address, listen_port))
    sock.settimeout(0.2)

    clients = []
    messages = []

    sock.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = accept_client(sock)
        except OSError:
            pass
        else:
            logger.info(f'established connection with address: {client_address}')
            clients.append(client)

        clients_to_receive = []
        clients_to_send = []

        if clients:
            try:
                clients_to_receive, clients_to_send, _ = select.select(clients, clients, [], 0)
            except OSError:
                pass
        if clients_to_receive:
            for cl in clients_to_receive:
                try:
                    msg = listen_and_get(cl)
                    process_client_message(msg, messages, cl)
                except Exception:
                    logger.info(f'Соединение с {cl.getpeername()} потеряно')
                    clients.remove(cl)
        if messages and clients_to_send:
            msg = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for wc in clients_to_send:
                try:
                    decode_and_send(wc, msg)
                except Exception:
                    logger.info(f'Соединение с {wc.getpeername()} потеряно')
                    clients.remove(wc)


if __name__ == '__main__':
    main_server()
