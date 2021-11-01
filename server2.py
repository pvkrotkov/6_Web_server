import socket
from os.path import isdir, isfile, relpath, abspath, normpath # импорт
from pathlib import Path as path
sock = socket.socket() # создание сокета
sock.bind(('', 80)) # привязка к порту 80
sock.listen(5)
conn, addr = sock.accept()
print("Connected", addr)
data = conn.recv(8192) # получение запроса
resp = """HTTP/1.1 """ # начало формирования ответа
msg = data.decode() # раскодирование запроса
msg = msg.split("\r\n")  # разбиение запроса на строки
line1 = msg[0].split(" ") # разбиение первой строки запроса по элементам
text = ""
if line1[1] == "/":
  line1[1] = abspath(".") # если передано /, преобразуем в папку сервера
line1[1] = path(line1[1]) # преобразуем файл в путь
if line1[0] == "GET": # если запрос "GET"
  if line1[1].exists(): # если существует
    resp += "200 Ok"  # код
    if line1[1].is_file():
      with open(line1[1], "r") as file:
        for i in file: # открытие и чтение файла
          text += i
    elif line1[1].is_dir():
      with open(line1[1].joinpath("index.html"), "r") as file: # если передана папка
        for i in file:
          text += i
  else: # если файла нет
    resp += "204 No Content"
elif line1[0] == "HEAD": # тела ответа не будет
  text = ""
elif line1[0] == "PUT" # если запрос PUT
  bodystart=msg.index("")+1 # ищем в теле запроса текст и добавляем его в соответствующий файл
  if line1[1].exists():
    if bodystart+1<len(msg)-1:
      resp += "204 No Content"
    else:
      print(msg)
      resp += "200 Ok"
  else:
    resp += "201 Created"
  with open(line1[1], "a") as file:
    for i in msg[bodystart::]:
      file.write(i)
elif line1[0] == "POST": # как PUT, но только файл создается заново
  resp += "200 Ok"
  bodystart=msg.index("")+1
  with open(line1[1], "w") as file:
    for i in msg[bodystart::]:
      file.write(i)
resp += "\n\r\n\r"+text # окончание формирования запроса
conn.send(resp.encode()) # отправка запроса
conn.close()
