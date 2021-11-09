import socket
from threading import Thread
import time


def create_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('', 8080))
            print("Using port 8080")
        except:
            sock.bind(('', 80))
            print("Using port 80")
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            thread = Thread(target=work, args=(conn,))
            thread.start()
            print("Connected", addr)
    except KeyboardInterrupt:
        sock.close()
        print('Server is closed...')


def work(conn):
    t = time.asctime(time.gmtime()).split(' ')
    t = f'{t[0]}, {t[2]} {t[1]} {t[4]} {t[3]} GMT'
    HDRS = f'HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1\nDate: {t}\nContent-Type: text/html; charset=utf-8\nConnection: close\n\n'
    HDRS_404 = f'HTTP/1.1 404 OK\nServer: SelfMadeServer v0.0.1\nDate: {t}\nContent-Type: text/html; charset=utf-8\nConnection: close\n\n'
    user_answer = conn.recv(1024).decode()
    print(user_answer)
    request = user_answer.split(" ")[1]
    if request == '/':
        with open('views/index.html', 'rb') as f:
            answer = f.read()
            conn.send(HDRS.encode('utf-8')+answer)
    else:
        try:
            with open('views'+request, 'rb') as f:
                answer = f.read()
                conn.send(HDRS.encode('utf-8')+answer)
        except FileNotFoundError:
            conn.send(HDRS_404.encode('utf-8')+"No page...".encode('utf-8'))


if __name__ == "__main__":
    create_socket()
