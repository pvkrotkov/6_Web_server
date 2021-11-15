import socket
import threading

def start_my_server():
    try:
        #создание сервера
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Привязываем сервер к порту
        server.bind(('', 80))
        server.listen(4)
        while True:
            print('Working')
            #Останавливающая операция (ждет подключения клиента)
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            #данные из файла
            content = load_page_from_request(data)
            #отправка содержимого в браузер
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        socket.close()
        print('Shutdown it')

def load_page_from_request(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    print(request_data)
    response = ''
    #Чтение файла
    try:
        with open('index.html', 'rb') as file:
            response = file.read() 
        return HDRS.encode('utf-8') + response
    except:
        #Отправка ошибки 404, если файл не найден
        return(HDRS_404 + 'Sorry, page not found. Error: 404').encode('utf-8')
        
if __name__=='__main__':
    threading.Thread(target=start_my_server, args=()).start()

