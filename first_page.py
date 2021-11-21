import http.server
import socketserver

PORT = 80
Handler = http.server.SimpleHTTPRequestHandler

#По умолчанию происходит поиск файла index.html в домашней директории и оправка его на указаный порт

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("запущено обслуживание порта: ", PORT)
    httpd.serve_forever()