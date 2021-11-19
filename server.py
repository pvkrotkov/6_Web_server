import socket
import os
from threading import Thread
import datetime
from os.path import exists, sep

def connection():
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
        print("Connected", addr)
        Thread(target=run, args=[conn, addr[0]]).start()

def run(conn, addr):
    dat = conn.recv(64000)
    msg = dat.decode()
    print(msg)
    site = data(msg, addr)
    conn.send(site)

def data(msg, addr):
    try:
        file = msg.split('\n')[0].split()[1][1:]
    except:
        file = "index.html"
    if not file:
        file = "index.html"
    site = os.getcwd() + sep + file
    if exists(site):
        with open(site, "rb") as s:
            ss = s.read()
        return f"HTTP/1.1 200 OK\n" \
                f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n" \
                f"Content-type: text/html\n" \
                f"Server: SelfMadeServer v0.0.1\n" \
                f"Content-length: {len(ss)}\n" \
                f"Connection: close\n" \
                f"\r\n\r\n".encode() + ss
    else:
        return ""


connection()