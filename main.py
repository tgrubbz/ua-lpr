#<main.py>
# LPR Main Program

# import modules
from constants import debug
import time
import imageProcessing
import characterDetector
import cv2
import numpy as np
import classifier as cs

# define the main function
def main():
    start = time.time()
    print('Starting LPR...')
    print('Debug mode ' + ('[ON]' if debug else '[OFF]'))
    
    # try to train
    cs.train()
    
    # open scene image
    img_scene = cv2.imread('/home/pi/Pictures/plate8.jpg')

    # check for successful image read
    if img_scene is None:
        print("img_scene could not be read")
        return

    if debug:
        cv2.namedWindow('img_scene', cv2.WINDOW_NORMAL)
        cv2.imshow('img_scene', img_scene)

    # get the threshold image
    img_thresh = imageProcessing.getImageThreshold(img_scene)
    src_thresh = img_thresh.copy()

    # get the character contours of interest (potential characters)
    contours_interesting = characterDetector.getContoursOfInterest(img_thresh)

    # get groups of contours (potential characters)
    group = characterDetector.groupContoursOfInterest(img_thresh.shape, contours_interesting)
    print 'DONE'
    if(group):
        print len(group)
        cs.detectCharacters(src_thresh, group)


    print 'time elapsed (sec): ' + str(time.time() - start)
    if debug:
        # wait until keypress
        cv2.waitKey(0)

    print 'Exiting LPR...'
    return
    
# ------------------ #
# call main function #
# ------------------ #
main()
