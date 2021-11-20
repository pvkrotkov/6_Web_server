import datetime as c_data
import os
from contextlib import closing
import socket
import threading

def protocoling(name, errorsInCode, date, ipAddr):
    f = open(logName, 'a')
    f.write(date + ' ' + ipAddr + ' ' + name + ' ' + errorsInCode + '\n')
    f.close()

def findOpenPort(ip_set):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((ip_set, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def editor():
    f.write(date + ' ' + customs[1] + ' ' + customs[0] + ' Server is running\n')
    print(f'Logging started!')

def fileReader(name):
    file = open(name, 'r')
    content = file.read()
    file.close()
    return content


customs = []
with open('settings.txt', 'r') as f:
    for i in f:
        customs.append(i.split(': ')[1][:-1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
customs[0] = int(customs[0])
customs[2] = int(customs[2])
try:

    sock.bind((customs[1], customs[0]))
    print(f"Yours address {customs[1]} {customs[0]}")

except OSError:

    customs[0] = findOpenPort(customs[1])
    print(f'The server port you selected is already in use.\nNew port: {customs[1]}{customs[0]}')
    sock.bind(('', customs[0]))
customs[0] = str(customs[0])
logName = 'logServer' + '_' + customs[1] + '_' + str(customs[0]) + '.txt'
date = str(c_data.datetime.date(c_data.datetime.today()))


try:

    with open(logName, 'a') as f:
        editor()

except FileNotFoundError:

    with open(logName, 'w') as f:
        editor()
sock.listen(1)


class WebServer(threading.Thread):
    def __init__(self, conn, addr, direct):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.ip = str(addr)
        self.connect()
        self.direct = direct
        self.clientHandeling()

    def connect(self):
        print(f'The connection came from: {self.addr}')

    def clientHandeling(self):
        while True:
            try:
                fl = self.conn.makefile('r')
            except ConnectionAbortedError:
                break
            msg = fl.readline(customs[2]).split()[1]
            if msg == '/':
                msg = '/index.html'
                fileType = 'html'
            else:
                try:
                    fileType = msg.split('.')[-1]
                except IndexError:
                    fileType = '-'
            fl = os.path.join(self.direct, msg[1:])
            if os.path.exists(fl) == True:
                if fileType == 'txt' or fileType == 'html':
                    fileType = 'text/html; charset = utf-8'
                    self.respond(fileReader(fl), msg, fileType, 'non_error')
                else:
                    self.respond("Error 403. The format is not supported", msg, fileType, '403')
            else:
                self.respond("Error 404. File not found", msg, fileType, '404')
        self.conn.close()

    def respond(self, resp, msg, fileType, err):
        logDate = str(c_data.datetime.date(c_data.datetime.today()))
        protocoling(msg, err, logDate, self.ip)
        lnRes = len(resp)
        resp = f"""HTTP/1.1 200 OK
Server: simple_http_server v0.0.1
Content-type: {fileType}
Date: {date}
Connection: close
Date: {date}
Content-length: {lnRes}
{resp}"""
        self.conn.send(resp.encode('utf-8'))

direct = os.getcwd()
while True:
    try:
        sockt = WebServer(*sock.accept(), direct)
        sockt.start()
    except:
        continue