import imp
import threading
import sys

listener = imp.load_source('listener', '/home/pi/Programs/ua-lpr/sockets/listener.py')
lpr = imp.load_source('lpr', '/home/pi/Programs/ua-lpr/lpr/lpr.py')

class processingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadId = 1

    def run(self):
        print 'Starting Processing Thread'
        lpr.start()
        print 'Ending Processing Thread'
        

class listeningThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadId = 2

    def run(self):
        print 'Starting Listening Thread'
        listener.start()
        print 'Ending Listening Thread'
        

def main():
    thread1 = processingThread()
    thread2 = listeningThread()

    thread1.start()
    thread2.start()
    

main()
