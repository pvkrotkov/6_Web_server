import socket

def generate_text(filename):


def foo(conn):
    data = conn.recv(8192 * 4)
    msg = data.decode()
    print(msg)
    resp = """HTTP/1.1 200 OK

Hello, webworld!"""
    conn.send(resp.encode())
    conn.close()


def main():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print(80)
    except OSError:
        sock.bind(('', 8080))
        print(8080)
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        foo(conn)


if __name__ == '__main__':
    main()
