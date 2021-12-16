import socket
from threading import Thread
import time


def server_start():
    sock = socket.socket()
    sock.bind(('', 80))
    print("<----------Сервер работает!---------->")
    sock.listen(5)
    while True:  # бесконечный цикл проверки портов
        conn, addr = sock.accept()
        thread = Thread(target=working, args=(conn, addr,))
        thread.start()


def working(conn, addr):
    print("Присоединился", addr)
    t = time.asctime(time.gmtime()).split(' ')
    t = f'{t[0]}, {t[2]} {t[1]} {t[4]} {t[3]}'  # красивый показ даты/времени
    print("Date: ", t)  # нужное задание - вывод даты
    h = f'HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1\nDate: {t}\nContent-Type: text/html; charset=utf-8\nConnection: close\n\n'  # шапка html
    user = conn.recv(1024).decode()
    rez = user.split(" ")[1]
    if rez == '/' or rez == '/index.html':  # случай с переходом на страницу index.html
        with open('index.html', 'rb') as f:
            answer = f.read()
            conn.send(h.encode('utf-8') + answer)  # везде должен быть utf-8, иначе вместо слов - иероглифы
    elif rez == "/next.html":  # случай с переходом на страницу next.html
        with open('next.html', 'rb') as f:
            answer = f.read()
            conn.send(h.encode('utf-8') + answer)
    else:  # отсутствие страниц
        resp = """HTTP/1.1 200 OK
        NOT FOUND"""
        conn.send(resp.encode('utf-8'))


server_start()