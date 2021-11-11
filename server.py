import socket
from threading import Thread
from datetime import datetime

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080


def handle_request(client_connection, client_address):

    request = client_connection.recv(8192).decode()
    print(f'Request: \n{request}')

    headers = request.split('\n')
    filename = headers[0].split()[1]
    if filename == '/':
        filename = 'index.html'

    try:
        page = open('pages/' + filename)
        content = page.read()
        page.close()

        headers = f'HTTP/1.1 200 OK\n\
        Server: SelfMadeServer v0.0.1\n\
        Date: {datetime.now()}\n\
        Content-Type: text/html; charset=utf-8\n\
        Connection: close\n\n'

        response = headers + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    client_connection.sendall(response.encode())


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))


    print(f'Listening on port {SERVER_PORT}')
    server_socket.listen(5)

    client_connection, client_address = server_socket.accept()

    user_thread = Thread(target=handle_request, args=(client_connection, client_address))
    user_thread.start()

    server_socket.close()


if __name__ == '__main__':
    main()
