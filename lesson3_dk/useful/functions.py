import json
import time
import logging
from variables import MAX_PACKAGE_LENGTH, ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
import portion as p
import socket
from decor import logger, log


#########client functions##################################
def decode_message(message: dict):
    logger.info(f'message has been decoded {message}')
    return json.dumps(message).encode(ENCODING)


def listen_and_get(client: socket.socket):
        while True:
            incoming_message_raw = client.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
            if incoming_message_raw:
                incoming_message = json.loads(incoming_message_raw)
                logger.debug(f'got message from sender {incoming_message}')
                if isinstance(incoming_message, dict):
                    return incoming_message


def decode_and_send(this_socket: socket.socket, message: dict):
    outgoing_message = decode_message(message)
    this_socket.send(outgoing_message)


def say_hello(account_name: str = 'guest'):
    resp = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.info(f'made a greeting message {resp}')
    return resp


#################common##################################################

def check_port(num: int):
    available_ports = p.open(1024, 65535)
    if num not in available_ports:
        logger.error(f'указанный порт не принаджежит диапазону 1024-65535 {num}')
        return 0
    return 1

###########server functions############################
