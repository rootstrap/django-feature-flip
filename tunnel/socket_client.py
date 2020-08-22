import socket
import threading
import requests
import json


def receive(connection):
    response = ''
    last_slash_character = False
    while (True):
        print('en t')
        print(connection)
        connection.recv(1024)
        character = str()
        print(connection)
        print('en k')
        print(f'{response} {character}')
        if (character == '\\'):
            last_slash_character = True
        elif (character == 'n' and last_slash_character):
            threading.Thread(target=receive, args=(response[:-1]))
            last_slash_character = False
            response = ''
        else:
            last_slash_character = False
            response += character
    print("Received: {}".format(response))


class SocketClient:
    class __OnlyOne:
        def __init__(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('takion-middleware', 9001))
                self.connection = sock
                # receive(connection)
                # sock.sendall(bytes('message', 'ascii'))
                # str(sock.recv(1024), 'ascii')
                # sock.sendall(bytes('message', 'ascii'))
                # sock.sendall(bytes('message', 'ascii'))
                # sock.close()
                while (True):
                    print('en t')
                    print(sock)
                    sock.recv(1024)

                # server_thread = threading.Thread(target=receive, args=(sock,))
                # sock.sendall(bytes('message', 'ascii'))
                # Exit the server thread when the main thread terminates
                # server_thread.daemon = True
                # server_thread.start()
    instance = None

    def __init__(self):
        if not SocketClient.instance:
            SocketClient.instance = SocketClient.__OnlyOne()
        else:
            SocketClient.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def send_message(self, json_data):
        json_string = json.dumps(json_data)
        stra = f"{json_string}\\n"
        print(stra, 'asaassas')
        print(self.instance.connection)
        self.instance.connection.sendall(b'sdsd')


def request_server(data):
    r = requests.post('http://web:8001/middleware/', data=json.loads(data))
    print(r.status_code, r.text)
