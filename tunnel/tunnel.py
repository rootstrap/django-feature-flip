import socket
import threading
import socketserver
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])
def connect_tunnel():
    takion_response = client('takion-middleware', 9001, 'self.data')
    return takion_response


@app.route('/status')
def status():
    return '{"online": True}'


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
        return response
