# LPR Main Program

# import modules
from constants import debug
import time
import cv2
import numpy as np
import threading
import imp
import picamera
from contour import *
import datetime

# Initailize the camera object
camera = picamera.PiCamera()

# Load sub directories
cs = imp.load_source('classifier', '/home/pi/Programs/ua-lpr/lpr/classifier.py')
characterDetector = imp.load_source('characterDetector', '/home/pi/Programs/ua-lpr/lpr/characterDetector.py')
imageProcessing = imp.load_source('imageProcessing', '/home/pi/Programs/ua-lpr/lpr/imageProcessing.py')
bt = imp.load_source('btComm', '/home/pi/Programs/ua-lpr/bt/btComm.py')
logger = imp.load_source('logger', '/home/pi/Programs/ua-lpr/sockets/logger.py')
db = imp.load_source('repo', '/home/pi/Programs/ua-lpr/dal/repo.py')

# Bluetooth sent command list
btCmds = dict()

# Thread for logging information to the server
class loggingThread(threading.Thread):
    def __init__(self, plate, access):
        threading.Thread.__init__(self)
        self.plate = plate
        self.access = access

    def run(self):
        print 'Starting Logging Thread'
        logger.logPlateAccess(self.plate, self.access)
        print 'Ending Logging Thread'
        
        
# Thread for sending commands via bluetooth to the Arduino
class bluetoothThread(threading.Thread):
    def __init__(self, access):
        threading.Thread.__init__(self)
        self.access = access

    def run(self):
        print 'Starting Bluetooth Thread'
        bt.sendAccess(self.access)
        print 'Ending Bluetooth Thread'
        

# Process the image at the given path
# Returns a string if the found plate or None
def process(path, singleExec):
    
    # open scene image
    img_scene_og = cv2.imread(path)

    # check for successful image read
    if img_scene_og is None:
        print("img_scene could not be read")
        return None

    if debug:
        cv2.namedWindow('img_scene', cv2.WINDOW_NORMAL)
        cv2.imshow('img_scene', img_scene_og)

    # Crops the image to the region of interest
    img_scene = imageProcessing.cropImage(img_scene_og)

    # get the threshold image
    img_thresh = imageProcessing.getImageThreshold(img_scene)
    src_thresh = img_thresh.copy()

    # get the character contours of interest (potential characters)
    contours_interesting = characterDetector.getContoursOfInterest(img_thresh)

    # get groups of contours (potential characters)
    group = characterDetector.groupContoursOfInterest(img_thresh.shape, contours_interesting)

    plate = None
    if(group):
        # get the detected string        
        plate = cs.detectCharacters(src_thresh, group)

    if debug:
        # wait until keypress
        cv2.waitKey(0)

    return plate
        

# Starts the processing loop
def start():
    print('Starting LPR...')
    print('Debug mode ' + ('[ON]' if debug else '[OFF]'))
    
    # train the classifier
    cs.train()

    # Start loop
    while(True):
        start = time.time()        

        camera.capture('scene.jpg')

        # Process
        plate = process('scene.jpg', False)
        print 'plate processed: ', plate
    
        if(plate):
            access = db.readAccess(plate)
            
##            logThread = loggingThread(plate, access)
##            logThread.start()

            # Remove old plates from btCmds
            now = datetime.datetime.now()
            for p in btCmds.keys():
                t = btCmds[p]
                if t < (now - datetime.timedelta(seconds = 30)):
                    del btCmds[p]

            # If the plate is not in the commands list
            # Then add it and send the command
            if(plate not in btCmds):
                btCmds[plate] = now
                btThread = bluetoothThread(access)
                btThread.start()
                
        print 'time elapsed (sec): ' + str(time.time() - start)

def main():
    # train the classifier
    cs.train()
    
    # Initailize the camera object    
    camera = picamera.PiCamera()    
    camera.capture('scene.jpg')    
    plate = process('scene.jpg', True)
    print 'plate: ', plate
    camera.close()


    
    
