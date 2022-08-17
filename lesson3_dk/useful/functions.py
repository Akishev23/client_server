import json
import time
from useful.variables import MAX_PACKAGE_LENGTH, ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
import portion as p
import socket


#########client functions##################################
def decode_message(message:dict):
    return json.dumps(message).encode(ENCODING)


def listen_and_get(client:socket.socket):
    while True:
        incoming_message_raw = client.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        incoming_message = json.loads(incoming_message_raw)
        if isinstance(incoming_message, dict):
            return incoming_message
        raise ValueError
    raise ValueError

def decode_and_send(this_socket:socket.socket, message:dict):
        outgoing_message = decode_message(message)
        this_socket.send(outgoing_message)


def say_hello(account_name:str='guest'):
    resp = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return resp
#################common##################################################

def check_port(num:int):
    available_ports = p.open(1024, 65535)
    if num not in available_ports:
        print('указанный порт не принаджежит диапазону 1024-65535')
        return 0
    return 1


###########server functions############################

