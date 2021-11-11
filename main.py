import socket
from datetime import datetime
import glob
import os
import threading


def sendClient(file_content, code, content_type, conn):
    """
    Генерируем заголовки для http-ответа
    Отправляем заголовки + тело ответа, если таковое имеется
    """
    http_answer = f"""HTTP/1.1 {code}
    Date: {datetime.now()}
    Content-Type: {content_type}
    Server: Seminar9
    Content-Length: {len(file_content.encode("utf-8"))}
    Connection: close\n"""

    print(http_answer)
    conn.send((http_answer+file_content).encode())
    conn.close()


def get(file_path, conn):
    """
        При обращении к корневой папке отдаём начальную страницу index.html
        Иначе передаём файл, к которому обратился пользователь
        Далее считываем содержимое и передаём в функцию отправки ответа сервера
    """
    if file_path == "/":
        # На будущие попытки для отправки нескольких файлов сразу. Тут буду пытаться отправить стили и картинки
        # для web-страницы
        # files = ["index.html", "styles/style.css"].extend(glob.glob("images/*"))
        files = "index.html"
        content_type = "text/html"
    else:
        files = file_path
        # Пока имею дело только с текстовыми или html файлами
        content_type = "text/html"

    # Проверяем, существует ли файл. Если да - читаем, код 200. Иначе - 404.
    if os.path.exists(files):
        with open(files, "r") as opened_file:
            content_file = opened_file.read()
        code = "200 OK"
    else:
        code = "404 Not Found"
        content_file = ""

    sendClient(content_file, code, content_type, conn)


def connected(sock):
    while True:
        conn, addr = sock.accept()
        print(f'Connected with : [{addr[0]}]--[{addr[1]}]')
        data = conn.recv(8192)
        msg = data.decode()
        print(msg)
        method, path, protocol = msg.split('\n')[0].split()
        # Изначально делал реализацию через pattern matching из python 3.10,
        # но не уверен, что у вас установелна последняя версия. Поэтому обычное ветвление.
        if method == "GET":
            get(path, conn)
        elif method == "POST":
            pass
        elif method == "HEAD":
            pass
        elif method == "PUT":
            pass
        elif method == "DELETE":
            pass
        elif method == "CONNECT":
            pass
        elif method == "OPTIONS":
            pass
        elif method == "TRACE":
            pass
        elif method == "PATCH":
            pass


def main():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print("Using port 80")
    except OSError:
        sock.bind(('', 8080))
        print("Using port 8080")

    sock.listen(5)
    while True:
        threads = [threading.Thread(target=connected, args=[sock]) for _ in range(5)]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


if __name__ == '__main__':
    main()

