import socket
import threading
import sys
from useful.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, \
    USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from useful.functions import check_port, listen_and_get, decode_and_send, decode_message
from json import JSONDecodeError


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

def accept_client(sock):
    while True:
        client, address = sock.accept()
        print(f'Client with address {address} connected')
        return client, address

def main_server():
    listen_port = DEFAULT_PORT
    listen_address = DEFAULT_IP_ADDRESS

    for index, name in enumerate(sys.argv):
        next = index + 1
        if name == '-p' and len(sys.argv) >= next + 1:
            listen_port = sys.argv[next]
        if name == '-a' and len(sys.argv) >= next + 1:
            listen_address = sys.argv[next]

    if not check_port(listen_port):
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_address, listen_port))
    sock.listen(MAX_CONNECTIONS)
    client = accept_client(sock)[0]

    message_from_client = listen_and_get(client)
    print(message_from_client)
    resp = process_client_message(message_from_client)
    print(resp)
    try:
        decode_and_send(client, resp)
    except (ValueError, JSONDecodeError):
        print('Invalid message format')
        client.close()


if __name__== '__main__':
        main_server()



