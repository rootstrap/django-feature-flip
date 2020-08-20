import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall("{\"logged\": true}")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9001
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
