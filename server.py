import socket
from datetime import datetime
import os
from threading import Thread








def sending_request(requested_file, conn): # заключительная функция, в ней пользователю, по его запросу, отправляются данные.
    date_time = (datetime.now())

    # Это доп. задание 1

    http200 = f"""HTTP/1.1 200 OK
    Date: {date_time}
    Server: SelfMadeServer v0.0.1
    Content-Type: text/html
    Content-Length: {len(requested_file)}
    Connection: close\n\n"""

    print(http200)
    file_to_send = http200 + requested_file

    conn.send(file_to_send.encode()) # сама отправка
    conn.close() # после onn.close() начинается новый проход бесконечного цикла.


def file_reader(requested_file, conn): # Функция file_reader по уже найденному в search_requested_file пути файла, открывает его на чтетение и в переменной content сохряняет содержимое.
    file = open(requested_file, 'r')
    content = file.read()
    
    file.close()
    sending_request(content, conn) # вызов следующей функции


def search_requested_file(msg, conn): # Функция необходимая для поиска файла из корневой директории файла, который должен отправиться по запросу клиенту.
    
    tmp_msg = (msg.split('\n'))
    tmp_msg2 = tmp_msg[0].split(' ') # Здесь из принятого запроса msg, я нахожу необходимый путь директории. Костыльный способ получился, но рабочий.
    
    
    if str(tmp_msg2[1]) == '/': # Опять костыли, можно было сделать намного рациональнее, но кроме как прохода по условиям, я не придумал способа лучше.
        requested_file = (os.getcwd()) + '/index.html' # в os.getcwd() определяется рабочая директория, в которой лежит сам код и файлы html, вообще все файлы для сервера.
        file_reader(requested_file, conn)
    elif str(tmp_msg2[1]) == '/fag.html':
        requested_file = (os.getcwd()) + '/fag.html'
        file_reader(requested_file, conn)
    elif str(tmp_msg2[1]) == '/nord.html':
        requested_file = (os.getcwd()) + '/nord.html'
        file_reader(requested_file, conn)
    elif str(tmp_msg2[1]) == '/index.html':
        requested_file = (os.getcwd()) + '/index.html'
        file_reader(requested_file, conn) # вызов следующей функции file_reader
        
    
def server_main(): # Основная функция, создания сервера, принятия подключения и запросов от клиентов.
    sock = socket.socket()
    sock.bind(('', 80))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print('Client Joined')
        print(f'Addres: {addr}')
        print(f'Conn: {conn}')
        data = conn.recv(8192)
        msg = data.decode()
        
        Thread(target=search_requested_file, args=[msg, conn]).start() # Реализовал такую логику в программе, что функции будут вызываться друг за другом. Многопоточность реализована.
        
        
if __name__ == '__main__': # Вызов главной функции. Решил сделать программу в бесконечном цикле.
    server_main()
