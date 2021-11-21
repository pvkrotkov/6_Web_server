import socket
from datetime import datetime
sock = socket.socket() # Создание сокета

def locate(dec_inf,conn):
    result=dec_inf.split('\n')[0].split()[1][1:] # Отбирание имени страницы из запроса
    send_this=f'HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1\nDate: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S GTM")}\nContent-Type: text/html; \nConnection: close\n\n'
    send_if_error=f'HTTP/1.1 400 ERROR \nServer:SelfMadeServer v0.0.1\nDate: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S GTM")}\nContent-Type: text/html; \Connection: close \n\n'
    if not result:
        with open('index.html','r') as file:
            info=file.read() # Считывание файла
            to_encode = send_this + info # Конкатенация (склеивание)
            conn.send(to_encode.encode())# Отправка ответа
    else:
        try:
            with open(result,'r') as file:
                info=file.read()
                to_encode=send_this+info
                conn.send(to_encode.encode())
        except FileNotFoundError:
            with open('404.html','r') as err:
                info=err.read()
                to_encode=send_if_error+info
                conn.send(to_encode.encode())

def manipulator(conn):
    inf=conn.recv(8192) # Получение запроса (по 8 КБ информации)
    dec_inf=inf.decode() # Перевод из битового представления
    locate(dec_inf,conn)

def server_starter():
    try:
        sock.bind(('', 80)) # Соединяем порт и сокет
        print("Using port 80")
    except OSError:
        sock.bind(('', 8080))
        print("Using port 8080")
    sock.listen(5) # Прослушивание порта
    while True:
        try:
            conn, addr = sock.accept() # Подтверждаем (принимаем) соединение
            print("Connected", addr)
            manipulator(conn)
        except KeyboardInterrupt:
            conn.close()
            break

if __name__=='__main__':
    server_starter()
