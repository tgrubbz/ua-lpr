import sys
from socket import *
import json
import imp

db = imp.load_source('repo', '/home/pi/Programs/ua-lpr/dal/repo.py')

debug = True

# Default host = this ip addr
# Arbitrary port
host = ''
port = 50007

# Create the socet
s = socket(AF_INET, SOCK_STREAM)

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind it to a host and port
s.bind((host, port))

# Returns the decoded request string
def getRequestString(conn):
    raw = conn.recv(2048)
    return raw.decode()

# Receive the request from the connection 
def receive(conn):
    while True:
        request = getRequestString(conn)
        if len(request) == 0:
            continue

        conn.sendall('success')
        data = json.loads(request)

        if 'addAccess' in data:            
            db.addAccess(data['addAccess'])

        if 'removeAccess' in data:
            db.removeAccess(data['removeAccess']['plate'])

        if 'updateAccess' in data:
            db.updateAccess(data['updateAccess'])
            
        if 'end' in data and data['end'] == True:
            return
        

def listen():
    # listen for one connection
    if debug:
        print 'listening...'
    s.listen(1)
    conn, addr = s.accept()

    if debug:
        print 'connection accepted', addr

    # Try to parse a request from the connection
    try:
        if debug:
            print 'parsing request...'
            
        receive(conn)

        if debug:
            print 'parsing complete'
    except:
        print 'Error: ', sys.exc_info()[0]
        raise


def start():
    print 'Starting  server'
    while True:
        listen()
