import socket
from wsgiref.handlers import format_date_time
from datetime import datetime
import threading


PAGES = 'pages'


def process_conn(conn):
    data = conn.recv(8192)
    msg = data.decode()

    print(msg)

    resource = PAGES + msg.split('\n')[0].split()[1]
    if resource == PAGES + '/':
        resource = resource + 'index.html'
    with open(resource) as file:
        content = file.read()    

    date = format_date_time(datetime.utcnow().timestamp())

    resp = f"""HTTP/1.1 200 OK
Date: {date}
Server: SelfMadeServer v0.0.1
Content-type: text/html
Content-length: {len(content.encode())}
Connection: close
{content}"""

    conn.send(resp.encode())

    conn.close()


sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen()

while True:
    conn, addr = sock.accept()
    print("Connected", addr)
    
    threading.Thread(target=process_conn, args=[conn]).start()
    
    