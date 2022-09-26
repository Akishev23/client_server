"""
server part of the project
"""
# -*- coding: utf-8 -*-
import socket
import select
from libr.variables import ACTION, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, \
    ERROR, MESSAGE_TEXT, MESSAGE, SENDER, RESPONSE_400, RECEIVER, EXIT
from libr.functions import listen_and_get, decode_and_send, args_parser
from decor import logger, log


@log
def process_client_message(message, messages, client, clients, names):
    """
    processing client's message
    :param names: dictionary, clients names and their socket objects
    :param clients: list of socket objects
    :param messages: list
    :param client: socket object
    :param message: dictionary
    :return: empty
    """

    presence_keys = [ACTION, TIME, SENDER]
    message_keys = [ACTION, TIME, RECEIVER, SENDER, MESSAGE_TEXT]
    exit_keys = [ACTION, SENDER]
    if all(message.get(key) for key in presence_keys) and message[ACTION] == PRESENCE:
        logger.debug(f'got correct message of presence from client {message}')
        name = message[SENDER]
        if name not in names.keys():
            logger.info('adding client to list of clients')
            names[name] = client
            decode_and_send(client, {RESPONSE: 200})
        else:
            resp = RESPONSE_400
            resp[ERROR] = 'Pointed name is busy'
            decode_and_send(client, resp)
            clients.remove(client)
            client.close()
        return

    if all(message.get(key) for key in message_keys) and message[ACTION] == MESSAGE:
        messages.append(message)
        logger.debug(f'got correct message from client {message}')
        return

    if all(message.get(key) for key in exit_keys) and message[ACTION] == EXIT:
        clt = names[message[SENDER]]
        clients.remove(clt)
        clt.close()
        del names[message[SENDER]]
        return

    resp = RESPONSE_400
    resp[ERROR] = f'query in wrong {message}'
    logger.error(f'got incorrect message from client {message}')
    decode_and_send(client, resp)
    return


def send_message_to_receiver(message, names, receiving_sockets):
    """
    function sends messages to recipients if needed
    :param message: dict
    :param names: dict
    :param receiving_sockets: list of socket objects
    :return: None
    """
    if message[RECEIVER] in names and names[message[RECEIVER]] in receiving_sockets:
        decode_and_send(names[message[RECEIVER]], message)
        logger.info(f'Sent message to {message[RECEIVER]} from user {message[SENDER]}')
        return
    if message[RECEIVER] in names:
        raise ConnectionError
    logger.error(f'User {message[RECEIVER]} is not registered, cannot send the message')


@log
def accept_client(sock):
    """
    accepting clients
    :param sock: socket object
    :return: tuple of socket object and client ip
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

    logger.info(f'Launching server with parameters port= {listen_port}, address ='
                f' {listen_address}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_address, listen_port))
    sock.settimeout(0.2)

    clients = []
    messages = []
    names = {}

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
            for clt in clients_to_receive:
                try:
                    msg = listen_and_get(clt)
                    process_client_message(msg, messages, clt, clients, names)
                except Exception:
                    logger.info(f'Connection with {clt.getpeername()} has been lost')
                    clients.remove(clt)
        if messages:
            for msg in messages:
                try:
                    send_message_to_receiver(msg, names, clients_to_send)
                except Exception:
                    logger.info(f'Unable to send message to {msg[RECEIVER]}')
                    clients.remove(names[msg[RECEIVER]])
                    del names[msg[RECEIVER]]
            messages.clear()


if __name__ == '__main__':
    main_server()
