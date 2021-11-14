import os
import socket
from datetime import datetime
from threading import Thread

class Server():

    def __init__(self):
        self.ip = ''

    def connection(self, conn, max_con = 13333):
        with conn:
            data = conn.recv(max_con)
            msg = data.decode()
            print(msg)
            request = self.create_status()
            request += self.response()
            conn.send(request)

    def response(self):
        ROOT_DIR = os.path.abspath(os.getcwd())
        file = 'index\index2.html'
        if os.path.exists(ROOT_DIR + os.sep + file):
            size = os.path.getsize(ROOT_DIR + os.sep + file)
            with open(ROOT_DIR + os.sep + file, "rb") as file:
                text = file.read()

            return f"Content-length: {size}\n" \
                f"\r\n\r\n".encode() + text

    def is_free_port(self, port):
        sock = socket.socket()
        sock.settimeout(3)
        try:
            sock.bind(('', port))
        except:
            return False
        else:
            return True
        finally:
            sock.close()

    def create_status(self):
        date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GTM")
        code = "200 OK"
        con = "keep-alive"
        status = f"""HTTP/1.1 {code}
        Server:SelfMadeServer v0.0.1
        Date: {date}
        Content-type: text/html
        Connection: {con}\n"""
        return status.encode()

    def sock_accept(self, socket):
        while True:
            conn, self.ip = socket.accept()
            print("Connected", self.ip)
            Thread(target=self.connection, args=[conn]).start()

    def main(self):
        initial_port = 80
        with socket.socket() as s:
            try:
                while True:
                    if self.is_free_port(initial_port):
                        print(f"Using port {initial_port}")
                        s.bind(('',initial_port))
                        break
                    else:
                        initial_port+=1
            except OSError:
                s.bind(('', 8080))
                print("Using port 8080")
            else:
                s.listen(5)
                while True:
                    conn, self.ip = s.accept()
                    print("Connected", self.ip)
                    Thread(target=self.connection, args=[conn]).start()



s = Server()
s.main()
