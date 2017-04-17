import socket
import json
from datetime import datetime
import time

#HOST = '192.168.137.63'
HOST = '192.168.43.160'
PORT = 8000
#PORT = 50007


def sendRequest(request):    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            
            # Send the JSON stringified log object
            s.sendall(json.dumps(request))
            
            # Await a response
            response = s.recv(1024)            
            s.close()
            break
        except:
            s.close()
            print 'socket logging error: ', error 
            time.sleep(1)
    

def logPlateAccess(plate, access):
    # Create the log object
    request = {}
    log = {}
    log['timestamp'] = datetime.now().isoformat()
    log['plate'] = plate
    log['access'] = access
    request['log'] = log
    request['end'] = True

    sendRequest(request)
