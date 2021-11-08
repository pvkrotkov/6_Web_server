import os
from threading import Thread
from datetime import datetime
import socket
from os.path import exists, sep
MAX = 16384

def handler(request, addr):
    directory = os.getcwd()
    try:
        current_file = request.split('\n')[0].split()[1][1:]
    except:
        current_file = 'index.html'
    if not current_file:
        current_file = 'index.html'
    if exists(directory + sep + current_file):
        with open(directory + sep + current_file, "rb") as file:
            text = file.read()
        return f"HTTP/1.1 200 OK\n" \
                f"Server: SelfMadeServer v0.0.1\n" \
                f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}\n" \
                f"Content-length: {len(text)}\n" \
                f"Content-type: text/html\n" \
                f"Connection: close\n" \
                f"\r\n\r\n".encode() + text


def connection(conn, addr):
    with conn:
        data = conn.recv(MAX)
        # if data == b"":
        #     conn.close()
        request = data.decode()
        print(request)
        resp = handler(request, addr)
        conn.send(resp)

def main():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print('Using port: ', 80)
    except OSError:
        sock.bind(('', 8080))
        print('Using port: ', 8080)
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        Thread(target=connection, args=[conn, addr[0]]).start()
        
if __name__ == '__main__':
    main()
