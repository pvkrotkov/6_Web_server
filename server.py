import os
import socket
from threading import Thread
import os

class Server():

    def __init__(self):
        self.ip = ''

    def connection(self, conn, max_con = 13333):
        with conn:
            data = conn.recv(max_con)
            msg = data.decode()
            print(msg)
            resp = self.response()
            conn.send(resp)

    def response(self):
        ROOT_DIR = os.path.abspath(os.getcwd())
        file = 'index\index2.html'
        if os.path.exists(ROOT_DIR + os.sep + file):
            with open(ROOT_DIR + os.sep + file, "rb") as file:
                text = file.read()
            return text

    def sock_accept(self, socket):
        while True:
            conn, self.ip = socket.accept()
            print("Connected", self.ip)
            Thread(target=self.connection, args=[conn]).start()

    def main(self):
        with socket.socket() as s:
            try:
                s.bind(('', 80))
                print("Using port 80")
            except OSError:
                s.bind(('', 8080))
                print("Using port 8080")
            else:
                s.listen(5)
                self.sock_accept(s)



s = Server()
s.main()
