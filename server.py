import socket
import datetime
#Для отправки времени

date = datetime.datetime.now()
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

resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

Hello, webworld! """ + str(date) + " Content-type: text/html " + "Server: SelfMadeServer v0.0.1 " + str(len(msg)) + " Connection: close"

conn, addr = sock.accept()
print("Connected", addr)
data = conn.recv(8192)
msg = data.decode()
print(msg)

#Единственный нюанс, я дважды отображаю в консоли содержание msg, но я сам хочу это оставить. P.S. Уберите строку print(msg)

conn.send(resp.encode())

conn.close()