import os
import socket
from threading import Thread
import hashlib

"""
shahar rosenthal
client
2 / 11 / 2022
"""

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
liba = str(os.cpu_count()) + '!'
DIGITS = 4
DATA_PER_CORE = 1000
ANSWER = ""


def prot_recv(client_socket):
    """
    returns the msg without the !
    :param: client_socket
    :return: the msg from the server without the !
    """
    res = ""
    data = ''
    while data != "!":
        res += data
        data = client_socket.recv(1).decode()
    return res


def check(start, crack_hash, digits):
    """
    checking every number of the range if he equals to the hash string
    :param start: the start of the range
    :param crack_hash
    :param digits
    :return: the answer
    """
    global ANSWER
    for i in range(start, start + DATA_PER_CORE):
        str2hash = str(i).zfill(digits)
        result = hashlib.md5(str2hash.encode())
        if result.hexdigest() == crack_hash:
            ANSWER = str2hash + '!'
            return ANSWER


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        hash_string = prot_recv(client_socket)
        # recv the hash string
        while ANSWER == "":
            threads = []
            client_socket.send(liba.encode())
            # sends to the server the liba's number
            start_range = prot_recv(client_socket)
            # recv the start of the range
            for i in range(os.cpu_count()):
                thread = Thread(target=check,
                                args=(int(start_range), hash_string, DIGITS))
                s = int(start_range)
                s += DATA_PER_CORE
                start_range = str(s)
                threads.append(thread)
                thread.start()
            for i in threads:
                i.join()
        client_socket.send(('a' + ANSWER).encode())

    except socket.error as err:
        print('error in communication with server - ' + str(err))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
