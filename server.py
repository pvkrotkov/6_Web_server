import socket
from threading import Thread

def working(conn, addr):
    print(f'{addr} was connected')

    user = conn.recv(1024).decode()
    print(user)
    request_from_server = user.split(" ")[1]
    if request_from_server == '/':
        with open('index.html', 'rb') as file:
            site = file.read()
            conn.send(site)
    if request_from_server == '/index.html':
        with open('index.html', 'rb') as file:
            site = file.read()
            conn.send(site)

    else:
        with open('error.html', 'rb') as file:
            site = file.read()
            conn.send(site)

            
sock = socket.socket()
try:
    sock.bind(('', 80))
except OSError:
    sock.bind(('', 8080))
print("Сервер запущен")
sock.listen(5)
while True:
    conn, addr = sock.accept()
    thread = Thread(target=working, args=(conn, addr,))
    thread.start()
