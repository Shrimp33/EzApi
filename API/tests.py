from api import *
from client import *
import threading

import os

# Start server in separate thread
db = DataServer(('localhost', 50000), BaseTCP)
server_thread = threading.Thread(target=db.serve_forever)
server_thread.start()

# Create client
a = Asker('localhost', 50000)

# Test push-get
try:
    a.ask('PUT', 'key', 'value')
    assert a.ask('GET', 'key') == 'value'
    print('Test push-get passed')
except AssertionError:
    print('Test push-get failed')

# Test push-get-delete
try:
    a.ask('PUT', 'key', 'value')
    assert a.ask('GET', 'key') == 'value'
    a.ask('DEL', 'key')
    assert a.ask('GET', 'key') == 'ERROR'
    print('Test push-get-delete passed')
except AssertionError:
    print('Test push-get-delete failed')

os._exit(0)