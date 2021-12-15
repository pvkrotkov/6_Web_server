import logging
import os
import socket
import utils
from datetime import datetime
from threading import Thread, Lock
from pprint import pprint


class Request:
    def __init__(self, data: bytes):
        self.text = []
        for i in data.decode("utf8", "replace").split("\n"):
            string = i.strip()
            if string:
                self.text.append(string)

    def get_info(self):
        return self.text[0].split(" ")


class Socket:
    def __init__(self, address: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.is_open = False

    def __repr__(self):
        return f"<ServerSocket {self.address}:{self.port}>"

    def open(self):
        log.info("Сокет открыт")
        self.sock.bind((self.address, self.port))
        self.is_open = True

    def close(self):
        log.info("Сокет закрыт")
        self.sock.close()

    def accept(self):
        self.sock.listen(5)
        self._connection, self._user_address = self.sock.accept()
        return self._connection, self._user_address

    def read_data(self):
        data = self._connection.recv(8192)
        print(data)
        text = []
        for i in data.decode("utf8", "replace").split("\n"):
            string = i.strip()
            if string:
                text.append(string)
        return text[0].split(" ")

    def send(self, data: bytes):
        self._connection.send(data)


class Server:
    def __init__(self, address="localhost", host=80):
        self.socket = Socket(address, host)
        self.clients = []

    def start(self):
        log.info("Начало работы сервера")
        self.socket.open()
        while True:
            self.clients.append(Client(self.socket.accept()))
            self.clients[-1].start()

    def stop(self):
        log.info("Сервер выключен")
        self.socket.close()

    def client_request(self):
        self.socket.accept()
        rd = self.socket.read_data()

        date = datetime.now()  # "Wed, 21 Oct 2015 07:28:00 GMT"
        content_length = 8000
        content_type = "text/html"
        server_html = "immortal-qQ 's server"

        response = "HTTP/1.1 200 OK\n" \
                   "Content-Type: {}\n" \
                   "Date: {}\n" \
                   "Content-length: {}\n" \
                   "Server: {}\n\n" \
                   "{}"

        if rd[1] == '/':
            rd[1] = "index.html"
        try:
            body = utils.read_file(rd[1])
            r = response.format(content_type, date, content_length, server_html, body)
        except FileNotFoundError:
            body = utils.read_file('404.html')
            r = response.format(content_type, date, content_length, server_html, body)
        self.socket.send(r.encode())


class Client(Thread):
    def __init__(self, sock):
        self.socket = sock
        self.conn = sock[0]
        self.addr = sock[1]
        Thread.__init__(self, name=str(self.addr[0]) + " " + str(self.addr[1]))

    def run(self):
        request = self.conn.recv(8192).decode()
        if request != '':
            headers = request.split('\n')
            webpage = headers[0].split()[1]

            if webpage == '/':
                webpage = '/index.html'
            elif '.' not in webpage:
                webpage += '.html'

            if webpage.split('.')[-1] in ALLOWED_FILES:
                try:
                    if webpage.split('.')[-1] == "jpg" or \
                            webpage.split('.')[-1] == "png" or \
                            webpage.split('.')[-1] == "jpeg":
                        with open("static/images/" + webpage, 'rb') as f:
                            content = f.read()
                        response = """HTTP/1.1 200 OK
                                Server: immortal-qQ-server
                                Content-type: image/png
                                Content-length: 5000
                                Connection: close\n\n"""
                    else:
                        body = utils.read_file(webpage.split('/')[-1])
                        response = "HTTP/1.1 200 OK\n" \
                                   "Content-Type: {}\n" \
                                   "Date: {}\n" \
                                   "Content-length: {}\n" \
                                   "Server: {}\n" \
                                   "Connection: close\n\n" \
                                   "{}"
                        date = datetime.now()  # "Wed, 21 Oct 2015 07:28:00 GMT"
                        content_length = 8000
                        content_type = "text/html"
                        server_html = "immortal-qQ 's server"
                        response = response.format(content_type, date, content_length, server_html, body)

                except FileNotFoundError:
                    response = "HTTP/1.1 200 OK\n" \
                               "Content-Type: {}\n" \
                               "Date: {}\n" \
                               "Content-length: {}\n" \
                               "Server: {}\n" \
                               "Connection: close\n\n" \
                               "{}"
                    date = datetime.now()  # "Wed, 21 Oct 2015 07:28:00 GMT"
                    content_length = 8000
                    content_type = "text/html"
                    server_html = "immortal-qQ 's server"
                    response = response.format(content_type, date, content_length, server_html,
                                               utils.read_file("404.html"))
            else:
                if webpage.split('.')[-1] != "ico":
                    response = "HTTP/1.0 403 FORBIDDEN\n" \
                               "Content-Type: {}\n" \
                               "Date: {}\n" \
                               "Content-length: {}\n" \
                               "Server: {}\n" \
                               "Connection: close\n\n" \
                               "{}"
                    date = datetime.now()  # "Wed, 21 Oct 2015 07:28:00 GMT"
                    content_length = 8000
                    content_type = "text/html"
                    server_html = "immortal-qQ 's server"
                    response = response.format(content_type, date, content_length, server_html,
                                               utils.read_file("403.html"))
                else:
                    response = utils.read_file("403.html")

            if "Content-type: image/png" in response:
                self.conn.sendall(response.encode() + content)
            else:
                self.conn.sendall(response.encode())

        self.conn.close()


logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("immortal-qQ-SERVER")
log = logging.getLogger("immortal-qQ-SERVER")

ALLOWED_FILES = ['html', 'js', 'png', 'jpg', 'jpeg']

if __name__ == "__main__":
    settings = utils.read_config()
    HOST, PORT = settings["ADDRESS"], settings["PORT"]

    server = Server(HOST, PORT)
    server.start()

# http://localhost:80/index.html
# http://localhost:80/cat.jpg
