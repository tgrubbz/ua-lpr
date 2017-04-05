import bluetooth as bt

# DT18Leo
addr = '98:D3:32:30:A7:19'

def sendAccess(access):
    sock = bt.BluetoothSocket(bt.RFCOMM)
    sock.connect((addr, 1))
    sock.send('o' if access else 'c')
    sock.close()





