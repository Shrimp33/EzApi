import socket
import pickle


HOST = 'localhost'
PORT = 8080

class Asker:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
    
    def ask(self, command, key = None, value = None):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps((command, key, value)))
            data = pickle.loads(s.recv(1024))
            return data