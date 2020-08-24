import socket
import threading
import requests
from flask import Flask, request
from socket_client import SocketClient
import json
import os


def request_server(data):
    r = requests.post('http://web:8000/middleware/', data=json.loads(data))
    print(r.status_code)


def receive_stream(client):
    response = ''
    while (True):
        character = str(client.recv(1), 'UTF-8')
        print(f"RECEIVED: {response}{character}")

        if (character == '\n'):
            threading.Thread(target=request_server, args=(response,)).start()
            print(f"SENT TO BE: {response}")
            response = ''
        else:
            response += character


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((os.environ.get('TAKION_IP'), int(os.environ.get('TAKION_PORT'))))
threading.Thread(target=receive_stream, args=(client,)).start()


app = Flask(__name__)


@app.route('/', methods=['POST'])
def connect_tunnel():
    print(request.json)
    string_to_send = f'{json.dumps(request.json)}\n'
    client.sendall(bytes(string_to_send, 'UTF-8'))
    return 'takion_response'
