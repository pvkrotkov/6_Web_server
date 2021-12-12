import os
import socket
from datetime import datetime
from threading import Thread

from settings import Settings


def addLog(text):
    with open('logs.txt', 'a') as file:
        file.write(text)


def process(req, addr):
    path = req.split('\n')[0].split(' ')[1][1:]
    if path == "":
        path = "index.html"
    path = Settings.DIRECTORY + os.sep + path

    ext = path.split('.')[-1]
    if ext == "":
        ext = "html"

    code = 200
    if not (os.path.exists(path) and os.path.isfile(path)):
        code = 404
    elif ext not in ["html", "css", "js", "png"]:
        code = 403

    fileType = "text/" + ext
    if ext == "png":
        fileType = "image/png"

    if code == 200:
        with open(path, 'rb') as file:
            body = file.read()
            length = len(body)
        resp = f"""HTTP/1.1 200 OK
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}
Server: SelfMadeServer v0.0.1
Content-Type: {fileType}
Content-Length: {length}
Connection: keep-alive

""".encode()
        resp += body
    else:
        resp = f"""HTTP/1.1 {code} {"Not found" if code == 404 else "Forbidden"}
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}
Server: SelfMadeServer v0.0.1
Content-Type: {fileType}
Content-Length: 0
Connection: keep-alive

""".encode()
    addLog(f"{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}, {addr}, {path}\n")
    return resp


def handle(conn, addr):
    req = conn.recv(4096).decode()
    print(req)
    if req != "":
        print(req)
        resp = process(req, addr)
        conn.send(resp)
    conn.close()


def main():
    sock = socket.socket()
    try:
        sock.bind((Settings.HOST, Settings.FIRST_PORT))
        print(Settings.HOST, Settings.FIRST_PORT)
    except OSError:
        sock.bind((Settings.HOST, Settings.SECOND_PORT))
        print(Settings.HOST, Settings.SECOND_PORT)
    sock.listen(4)
    while True:
        conn, addr = sock.accept()
        print(f'Connected: {addr}\n')
        newThread = Thread(target=handle, args=[conn, addr[0]])
        newThread.start()


if __name__ == '__main__':
    main()
