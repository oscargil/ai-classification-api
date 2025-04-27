from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
import socket

class CustomWSGIServer(WSGIServer):
    def server_bind(self):
        """Override server_bind to skip the getfqdn call"""
        self.socket.bind(self.server_address)
        self.server_name = '127.0.0.1'
        self.server_port = self.server_address[1]

def run(addr, port, wsgi_handler):
    server_address = (addr, port)
    httpd = CustomWSGIServer(server_address, WSGIRequestHandler)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever() 