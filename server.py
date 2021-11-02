import re
import socket
import json
from os.path import exists, sep
from threading import Thread
from datetime import datetime

LOGS = "logs.txt"
SETTINGS = "settings.json"
with open(SETTINGS, "r") as settings_file:
    settings = json.load(settings_file)


def write_log(addr, text, is_error):
    with open(LOGS, "a") as log_file:
        log_file.write(f"""Date: {datetime.now().timestamp()}
IP-address: {addr}
{'Error' if is_error else 'File path'}: {text}

""")


def generate_path(request, addr):
    global settings
    try:
        filename = request.split("\n")[0].split(" ")[1]
    except:
        filename = "index.html"
    if filename == "/":
        filename = "index.html"
    if not exists(settings["directory"] + sep + filename) or filename == "":
        write_log(addr, "404", True)
        return "404"
    elif not re.match(r"\S*\.((html)|(css)|(js))", filename):
        write_log(addr, "403", True)
        return "403"
    else:
        write_log(addr, settings["directory"] + sep + filename, False)
        return settings["directory"] + sep + filename


def generate_text(request, addr):
    path = generate_path(request, addr)
    if path == "403" or path == "404":
        return path
    else:
        with open(path, "r") as text:
            return "\n".join([str(lines) for lines in text.readlines()])


def generate_response(request, addr):
    text = generate_text(request, addr)
    if text == "403" or text == "404":
        return f"""HTTP/1.1 {text} {"Not found" if text == "404" else "Forbidden"}
Server: SelfMadeServer v0.0.1
Date: {datetime.now().timestamp()}
Content-Type: text/html
Content-Length: {len(text)}
Connection: close

""".encode()
    else:
        return f"""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Date: {datetime.now().timestamp()}
Content-Type: text/html
Content-Length: {len(text)}
Connection: close

{text}""".encode()


def handle(conn, addr):
    global settings
    with conn:
        request = conn.recv(settings["size"]).decode()
        print(request)
        response = generate_response(request, addr)
        print(response)
        conn.send(response)


def main():
    global settings
    sock = socket.socket()
    try:
        sock.bind(('', settings["port"]))
        print(settings["port"])
    except OSError:
        sock.bind(('', settings["alternate_port"]))
        print(settings["alternate_port"])
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        Thread(target=handle, args=[conn, addr[0]]).start()


if __name__ == '__main__':
    main()
