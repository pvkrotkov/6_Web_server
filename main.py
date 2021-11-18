import socket, random, datetime

sock = socket.socket()
port = 12345

try:
    sock.bind(('', 12345))
    print('Used port:', port)
except OSError:
    port = random.randint(1024, 65535)
    sock.bind(('', port))
    print('Used port:', port)

sock.listen(5)
conn, addr = sock.accept()
print(f'{addr} connected')


data = conn.recv(8192)
print(data.decode())

content = 'HI WEBWORLD!!!'
msg = f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nContent-type: text/html (utf-8)\nServer: localhost:{port}\nContent-length: {len(content)}\nConnection: close\n\n{content}"

if not msg:
    f = open('index.html')
    txt = f.read()
    conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    for i in range(0, len(txt)):
        conn.send(txt[i].encode())
    conn.send('\r\n'.encode())
else:
    conn.send(f"""HTTP/1.1 200 OK\r\n\r\n{msg}""".encode())


conn.close()