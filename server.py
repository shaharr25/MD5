import socket
from threading import Thread, Lock
import select

"""
shahar rosenthal
server
2 / 11 / 2022
"""
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
hash_string = "EC9C0F7EDCC18A98B1F31853B1813301"
start_range = 0
lock = Lock()
FLAG = 0


def prot_recv(client_socket):
    """
    returns the msg without the !
    :param: client_socket:
    :return: the msg from the client without the !
    """
    res = ""
    data = ''
    while data != "!":
        res += data
        data = client_socket.recv(1).decode()
    return res


def handle_connection(client_socket, client_address):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    global start_range
    global lock
    global FLAG
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        # handle the communication
        msg = hash_string + '!'
        client_socket.send(msg.encode())
        while FLAG == 0:
            range_msg = str(start_range) + '!'
            # sends the hash string to the clients
            liba = prot_recv(client_socket)
            # rcv from the client the number of libot he has
            lock.acquire()
            client_socket.send(range_msg.encode())
            # sends to the client the start of his range
            start_range += int(liba)*10000000
            # change the start range to the next client
            lock.release()
            answer = prot_recv(client_socket)
            if answer[0] == 'a':
                # recv the answer from the client and checks if this is really the answer and not another msg
                FLAG = 1
                print(answer[1:])

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        threads = []
        while not FLAG:
            rlist, wlist, xlist = select.select([server_socket], [], [], 0.1)
            if rlist:
                client_socket, client_address = server_socket.accept()
                thread = Thread(target=handle_connection,
                                args=(client_socket, client_address))
                threads.append(thread)
                thread.start()
        for i in threads:
            i.join()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
