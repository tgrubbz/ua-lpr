import imp
import threading
import sys

listener = imp.load_source('listener', '/home/pi/Programs/ua-lpr/sockets/listener.py')
lpr = imp.load_source('lpr', '/home/pi/Programs/ua-lpr/lpr/lpr.py')

lpr.main()
