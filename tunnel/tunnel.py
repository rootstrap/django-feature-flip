import socket
import threading
import socketserver
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    takion_response = client('localhost', 9001, 'self.data')
    return 'Hello, World!'


@app.route('/status')
def hello_world():
    return '{"online": True}'


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
        return response
