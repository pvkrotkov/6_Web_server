import socket
import datetime

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

print(msg)


nowdate = datetime.datetime.utcnow().strftime(r"%a, %d %b %Y %H:%M:%S GMT")
print(nowdate)
content = "Hello, webworld!"
content_length = len(content)
resp = f"""HTTP/1.1 200 OK
Date: {nowdate}
Content-length: {content_length}
Server: SelfMadeServer v0.0.1
Content-type: text/html; sharset = utf8
Connection: close

{content}"""

conn.send(resp.encode())

conn.close()