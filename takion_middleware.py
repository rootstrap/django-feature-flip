# Echo server program
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 9001))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = str(conn.recv(1024), 'UTF-8')
            if (data):
                print(f'received {data}')
                js = "{\"as\":\"as\"}\n"
                stra = f"{data}{js}"
                conn.sendall(bytes(stra, 'UTF-8'))
