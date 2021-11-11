import http.server
import socketserver

port = 8080
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", port), handler) as web_server:
    print(f'Serving at port: {port}')
    web_server.serve_forever()
