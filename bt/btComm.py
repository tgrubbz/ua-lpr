import bluetooth as bt
import time

# DT18Leo
addr = '98:D3:32:30:A7:19'

def sendAccess(access):
    while True:
        try:
            sock = bt.BluetoothSocket(bt.RFCOMM)
            sock.connect((addr, 1))
            print 'access: ', access
            sock.send('o' if access else 'c')
            sock.close()
            break
        except bt.btcommon.BluetoothError as error:
            sock.close()
            print 'bluetooth error: ', error 
            time.sleep(1)
            





