from doctest import Example
import socketserver
import pickle
import threading


# Create listener for server on socket server port 8080
class BaseTCP(socketserver.BaseRequestHandler):
    def handle(self):
        # Get data from client
        data = self.request.recv(1024)
        data = pickle.loads(data)
        # Command tree
        if data[0] == 'ping':  # ping pong
            self.request.sendall(pickle.dumps('pong'))
        if data[0] == "GET":
            # Get data from server
            data = self.server.get(data[1])
            # Send data to client
            self.request.sendall(pickle.dumps(data))
        elif data[0] == "PUT":
            # Put data to server
            self.server.put(data[1], data[2])
            # Send data to client
            self.request.sendall(pickle.dumps('OK'))
        elif data[0] == "DEL":
            # Delete data from server
            self.server.del_(data[1])
            # Send data to client
            self.request.sendall(pickle.dumps('OK'))
        else:
            # Throw error
            self.request.sendall(pickle.dumps("ERROR"))
# Create server class

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Define server REST commands
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
    # Get data from server
    def get(self, key):
        return NotImplementedError
    # Put data to server
    def put(self, key, value):
        return NotImplementedError
    # Delete data from server
    def del_(self, key):
        return NotImplementedError

class DataServer(ThreadedTCPServer):
    # Define server REST commands
    def __init__(self, server_address, RequestHandlerClass):
        ThreadedTCPServer.__init__(self, server_address, RequestHandlerClass)
        self.data = {}
    # Get data from server
    def get(self, key):
        return self.data.get(key, "ERROR")
    # Put data to server
    def put(self, key, value):
        self.data[key] = value
    # Delete data from server
    def del_(self, key):
        del self.data[key]

# Create server
server = DataServer(('localhost', 8080), BaseTCP)
# Start server
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
