import socket
from threading import Thread
import time


def create_server():
    # создание сервера и привязка его к порту
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 70))
    print("Using port 80")
    print("сервер  запущен!")
    sock.listen(5)
    conn, addr = sock.accept()
    thread = Thread(target=web_page, args=(conn, addr,))
    thread.start()


def web_page(conn, addr):
    print('кто присоединился:', addr)

    datetime = time.asctime(time.gmtime()).split(' ')
    datetime = f'{datetime[0]}, {datetime[2]} {datetime[1]} {datetime[4]} {datetime[3]}'
    print("Дата: ", datetime)
    resp = f'HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1\nDate: {datetime}\nContent-Type: text/html; charset=utf-8\nConnection: close\n\n'
    user = conn.recv(1024).decode()
    res = user.split(" ")[1]

    # Чтение файла
    if res == '/' or res == '/index.html':
        with open('index.html', 'rb') as f:
            answer = f.read()
            conn.send(resp.encode('utf-8') + answer)

    else:

        conn.send(("""HTTP/1.1 200 OK
        NOT FOUND.ERROR 404""").encode('utf-8'))


create_server()