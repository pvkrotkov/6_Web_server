import socket

resp = """HTTP/1.1 200 OK
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """
err_resp = """HTTP/1.1 404 OK
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """

def start_server():
    global resp
    try:
        # запуск сервера
        sock = socket.socket()
        try:
            sock.bind(('localhost', 80))
            print("Using port 80")
        except OSError:
            sock.bind(('localhost', 8080))
            print("Using port 8080")
        sock.listen(5)
        while True:
            #ожидание сервера
            conn, addr = sock.accept()
            # обработка сообщения
            data = conn.recv(8192).decode('utf-8')
            if data.split(' ')[1]!=('/exit'):
                content = load_page(data)
                # отправка сообщения
                conn.send(content)
                conn.close()
            else:
                break
                conn.send(resp.encode('utf-8')+'Shutting down'.encode())
                sock.close()
                print('Shutdown')
    except:
        sock.close()
        print("Shutting down.")

def load_page(req_data):
    global resp, err_resp
    path = req_data.split(' ')[1]
    path = path[1:]
    response = ''
    try:
        with open(path, 'rb') as file:
            response = file.read()
        return resp.encode('utf-8')+response
    except FileNotFoundError:
        return (err_resp+"Sorry, Page Not Found").encode('utf-8')

if __name__ == '__main__':
    start_server()