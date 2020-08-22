# Echo server program
import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 9001))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)

            json_string = '{"as":"asas"}'
            stra = f"{json_string}\\n{json_string}\\n"
            if not data:
                break
            conn.sendall(bytes(stra, 'ascii'))
            time.sleep(5)
