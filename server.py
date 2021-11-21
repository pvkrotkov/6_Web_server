import socket
from datetime import datetime
from threading import Thread

def vkl_serv():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print("Using port 80")
    except OSError:
        sock.bind(('', 8080))
        print("Using port 8080")

    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        thread = Thread(target=veb, args=(conn, addr))
        thread.start()

def veb(conn, addr):
    h = f'HTTP/1.1 200 OK\n\
             Server: SelfMadeServer v0.0.1\n\
             Date: {datetime.now()}\n\
             Content-Type: text/html; charset=utf-8\n\
             Connection: close\n\n'
    er="""HTTP/1.1 404 
    NOT FOUND"""
    user = conn.recv(1024).decode()
    path = user.split(" ")[1]
    if path == '/':
        with open('index.html', 'rb') as file:
            ht = file.read()
            conn.send(h.encode('utf-8') + ht)
    else:
        conn.send(er.encode('utf-8'))

if __name__ == "__main__":
        vkl_serv()
