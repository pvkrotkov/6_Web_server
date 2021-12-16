import socket
from datetime import datetime

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()

print(msg, end = '')


content = ''
with open('index.html', 'r', encoding='utf-8') as f:
    for line in f:
        content += line
content_length = len(content)

resp = f"""HTTP/1.1 200 OK
Date: {datetime.now()}
Content-length: {content_length}
Server: SelfMadeServer v0.0.1
Content-type: text/html, charset = utf8
Connection: close

{content}"""

conn.send(resp.encode())

conn.close()