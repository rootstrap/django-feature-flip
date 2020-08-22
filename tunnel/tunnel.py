from flask import request
import socket
import threading
import requests
from flask import Flask
from socket_client import SocketClient
import json

import socket
import threading

# SERVER = "127.0.0.1"
# PORT = 8080


def request_server(data):
    r = requests.post('http://web:8000/middleware/', data=json.loads(data))
    print(r.status_code)


def receive_stream(client):
    response = ''
    last_slash_character = False
    while (True):
        character = str(client.recv(1), 'ascii')
        client.sendall(bytes("This is from Client", 'UTF-8'))
        # print(character)
        if (character == '\\'):
            last_slash_character = True
        elif (character == 'n' and last_slash_character):
            threading.Thread(target=request_server, args=(response,)).start()
            # server_thread.daemon = Fa
            # server_thread.start()
            print(response)
            last_slash_character = False
            response = ''
        else:
            last_slash_character = False
            response += character


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('takion-middleware', 9001))
client.sendall(bytes("This is from Client", 'UTF-8'))
threading.Thread(target=receive_stream, args=(client,)).start()


app = Flask(__name__)
# client = SocketClient()


@app.route('/', methods=['POST'])
def connect_tunnel():
    print(request.json)
    print(request.data)
    print('NADA?')
    print(request.__dict__)
    client.sendall(bytes(f'{json.dumps(request.json)}\n', 'UTF-8'))
    return 'takion_response'


# @app.route('/status')
# def status():
#     return '{"online": True}'


# SERVER = "127.0.0.1"
# PORT = 8080


# def request_server(data):
#     r = requests.post('http://web:8000/middleware/', data=json.loads(data))
#     print(r.status_code)


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('takion-middleware', 9001))
# client.sendall(bytes("This is from Client", 'UTF-8'))
# response = ''
# last_slash_character = False
# while (True):
#     character = str(client.recv(1), 'ascii')
#     client.sendall(bytes("This is from Client", 'UTF-8'))
#     # print(character)
#     if (character == '\\'):
#         last_slash_character = True
#     elif (character == 'n' and last_slash_character):
#         threading.Thread(target=request_server, args=(response,)).start()
#         # server_thread.daemon = Fa
#         # server_thread.start()
#         print(response)
#         last_slash_character = False
#         response = ''
#     else:
#         last_slash_character = False
#         response += character
# # client.close()
