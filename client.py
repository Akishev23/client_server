"""
clint's part of messager
"""
# -*- coding: utf-8 -*-
import json
import time
import socket
import sys
from libr.functions import listen_and_get, decode_and_send, say_hello, args_parser
from libr.variables import MESSAGE, MESSAGE_TEXT, TIME, ACTION, ACCOUNT_NAME, SENDER, ERROR, \
    RESPONSE
from decor import logger, log
from libr.errors import ServerError


@log
def read_message(message):
    """
    reading messages dictionary
    :param message: dictionary
    :return: nothing
    """
    checking_key = [ACTION, SENDER, MESSAGE_TEXT]
    if all(message.get(key) for key in checking_key) and message.get('action') == MESSAGE:
        logger.info(f'got message {message[SENDER]}' "\n"
                    f'--------------------------------------------'
                    f'{message[MESSAGE_TEXT]}')
        print(message.get(MESSAGE_TEXT))
    else:
        logger.info(f'wrong format of the message'
                    f'{message}')


@log
def form_message(socket_that: socket.socket, name):
    """
    making message before sending it
    :param socket_that: socket object
    :param name: str
    :return: message dictionary
    """
    message = input('input message or "exit" to quit: "\n"')
    if message == 'exit':
        socket_that.close()
        logger.info('closing connection')
        sys.exit()
    ms_ready = {
        ACTION: 'message',
        TIME: time.time(),
        ACCOUNT_NAME: name,
        MESSAGE_TEXT: message
    }
    logger.debug('message procecced')
    return ms_ready


@log
def hello_answer(message):
    """
    'Reading answer from server when "hello" is sent
    :param message: dictionary
    :return: status of response
    """
    if message and RESPONSE in message:
        if message.get(RESPONSE) == 200:
            return '200 : ok'
        raise ServerError(f'{message[ERROR]}')


@log
def main_loop():
    """
    client's part of the program
    :return: nothing
    """
    address, port, mode, name = args_parser()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    logger.info(f'client with keys {address} - {port} - {mode} - {name} launched')
    try:
        greeting = say_hello(name)
        decode_and_send(sock, greeting)
        listened = listen_and_get(sock)
        answer = hello_answer(listened)
        logger.info(f'got server"s approve, {answer}')
        print(f'got server"s approve, {answer}')
    except json.JSONDecodeError:
        logger.error('Unable to decode the message')
        sys.exit(1)
    except ServerError as error:
        logger.error(f'Error of the server, {error}')
    except ConnectionRefusedError:
        logger.error('Connection has been refused')
        sys.exit(1)
    else:
        print(f'mode - {mode}')
        while True:
            if mode == 'send':
                try:
                    message = form_message(sock, name)
                    decode_and_send(sock, message)
                except Exception:
                    logger.exception('exception got')
                    sys.exit(1)
            else:
                try:
                    message = listen_and_get(sock)
                    read_message(message)
                except Exception:
                    logger.exception('exception got')
                    sys.exit(1)


if __name__ == '__main__':
    main_loop()
