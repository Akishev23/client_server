"""
clint's part of messager
"""
# -*- coding: utf-8 -*-
import json
import time
import socket
import sys
import threading
from libr.functions import listen_and_get, decode_and_send, say_hello, args_parser
from libr.variables import MESSAGE, MESSAGE_TEXT, TIME, ACTION, SENDER, ERROR, \
    RESPONSE, EXIT, RECEIVER
from libr.errors import ServerError
from decor import logger, log


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
    receiver = input('Input to whom message is addressed \n')
    message = input('input message \n')
    ms_ready = {
        ACTION: 'message',
        SENDER: name,
        RECEIVER: receiver,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    logger.info('message processed')
    try:
        decode_and_send(socket_that, ms_ready)
        logger.info(f'message for {receiver} from {name} has been successfully sent')
    except Exception:
        logger.exception('exception')
        sys.exit(1)


@log
def hello_answer(message):
    """
    Reading answer from server when "hello" is sent
    :param message: dictionary
    :return: status of response
    """
    if message and RESPONSE in message:
        if message.get(RESPONSE) == 200:
            return '200 : ok'
        raise ServerError(f'{message[ERROR]}')


@log
def create_exit_message(name):
    """
    creating notification regarding exit
    :param name: str
    :return: None
    """
    return {
        ACTION: EXIT,
        TIME: time.time(),
        SENDER: name
    }


@log
def getting_message_from_server(sock, name):
    """
    function which handles the messages from server
    :param sock: socket object
    :param name: str
    :return: None
    """
    while True:
        try:
            msg = listen_and_get(sock)
            check_dict = [ACTION, SENDER, RECEIVER, MESSAGE_TEXT]
            if all(msg.get(key) for key in check_dict) and msg[ACTION] == 'message' and \
                    msg[RECEIVER] == name:
                print(f'Message from user {msg[SENDER]}:'
                      f'\n {msg[MESSAGE_TEXT]}')
            else:
                logger.error(f'Wrong format of message from server: {msg}')
        except Exception:
            logger.exception('exception, see further')


@log
def get_help():
    print('Admissible commands')
    print('message - type your message')
    print('help - print help')
    print('exit - exit')


@log
def user_helper(sock, name):
    """
    function which asks for command and sends messages
    :param sock: socket object
    :param name: str
    :return: None
    """
    get_help()
    while True:
        command = input('Input command \n')
        if command == 'message':
            form_message(sock, name)
        elif command == 'help':
            get_help()
        elif command == 'exit':
            decode_and_send(sock, create_exit_message(name))
            print('connection is closed')
            logger.info('connection is closed according to users command')
            time.sleep(0.5)
            break
        else:
            print('Could not recognize command')


@log
def main_loop():
    """
    client's part of the program
    :return: nothing
    """
    print('Messager')
    address, port, mode, name = args_parser()
    if not name:
        name = input('input your name')
    print(f'Your nickname is: {name}')
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
    except (ConnectionRefusedError, ConnectionError):
        logger.error('Connection has been refused')
        sys.exit(1)
    else:
        print('Messager')
        print(f'Your nickname is: {name}')

        rec = threading.Thread(target=getting_message_from_server, args=(sock, name),
                               daemon=True)
        rec.start()
        user_int = threading.Thread(target=user_helper, args=(sock, name), daemon=True)
        user_int.start()
        logger.info('all processed are launched')

        while True:
            time.sleep(0.5)
            if rec.is_alive() and user_int.is_alive():
                continue
            break


if __name__ == '__main__':
    main_loop()
