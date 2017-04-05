import socket
import json
from datetime import datetime

#HOST = '192.168.137.63'
HOST = '192.168.43.160'
PORT = 8000
#PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def openConnection():
    # Connect to the server
    s.connect((HOST, PORT))
    

def closeConnection():
    # Close the connection
    s.close()    
    

def logPlateAccess(plate, access):
    # Create the log object
    request = {}
    log = {}
    log['timestamp'] = datetime.now().isoformat()
    log['plate'] = plate
    log['access'] = access
    request['log'] = log
    request['end'] = True

    # Open the connection
    openConnection()

    # Send the JSON stringified log object
    s.sendall(json.dumps(request))

    # Await a response
    response = s.recv(1024)

    # End the connection
    closeConnection()

    # Print the response
    print 'Response: ', repr(response)
