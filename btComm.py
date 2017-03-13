
import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))
    print bluetooth.find_service(address=addr)
    if name == 'DT18Leo':
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((addr, 1))
        print 'sending info...'
        sock.send('some info')
        print 'info sent...'
        sock.close()
        print 'socket closed...'





