import cv2
import numpy as np
import imp
from contour import * 

cd = imp.load_source('characterDetector', '/home/pi/Programs/ua-lpr/lpr/characterDetector.py')

kn = cv2.ml.KNearest_create()

def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1 , ncols)
            .swapaxes(1, 2)
            .reshape(-1, nrows, ncols))

def viewTrainingData():
    flattened = np.loadtxt("flattened_images.txt", np.float32)
##    print 'flat shape: ', flattened.shape
##    flattened[i].reshape( (30,20) )

    chars = ''
    for i in range(0, len(flattened)):
        flat = flattened[i].reshape((20,30)).reshape((1, 20*30))
        _, results, _, _ = kn.findNearest(flat, k = 1)
        char = str(chr(int(results[0][0])))
        chars += char        

    print 'flattened characters: ', chars 
    

def train():
    classifications = np.loadtxt("classifications.txt", np.float32)
    flattened = np.loadtxt("flattened_images.txt", np.float32) 
    
    classifications = classifications.reshape((classifications.size, 1))
    kn.setDefaultK(1)
    
    kn.train(flattened, cv2.ml.ROW_SAMPLE, classifications)

    viewTrainingData()


def adjustPerspective(img, rect, i):
    bpts = cv2.boxPoints(rect)
    print 'p box points: ', bpts
    pts1 = np.float32([ bpts[1], bpts[2], bpts[0], bpts[3] ])
    pts2 = np.float32([ [0,0], [20,0], [0,30], [20,30] ])

    h, status = cv2.findHomography(pts1,pts2)
    dst = cv2.warpPerspective(img, h, (20,30))

##    cv2.namedWindow('perspective transform: ' + str(i), cv2.WINDOW_NORMAL)
##    cv2.imshow('perspective transform: ' + str(i), dst)
    return dst

def thresholdArray(arr):
    array_np = np.asarray(arr)

    low_nums = array_np < 127
    array_np[low_nums] = 0
    
    high_nums = array_np >= 127
    array_np[high_nums] = 255
    return array_np


# Creates a file for the data captured
#
# If you want to add the parsed data to the training data,
#   then copy the corresponding row from the created file
#   and append it to the new master training data file.
def createTrainingData(rois):
    np.savetxt('currentParseData.txt', [])
    f = open('currentParseData.txt', 'w')
    for i in range(0, len(rois)):
        np.savetxt(f, np.float32(rois[i].reshape((1, 20*30))))
    f.close()

    


def detectCharacters(thresh, group):
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # sort the contours by their bounding box's x-coord
    group = sorted(group, key = lambda cnt: cnt.rect[0][0])
    
    string = ""
    rois = []
    i = 0
    for cnt in group:        
        (x, y), (w, h), angle = cnt.rect

        roi = thresh[y - h/2 - 0: y + h/2 + 0, x - w/2 - 0: x + w/2 + 0]
        roi_resized = cv2.resize(roi, (20, 30))        
        roi_shaped = roi_resized.reshape((1, 20*30))
        roi_shaped = np.float32(roi_shaped)

        ret, results, neighbors, dist = kn.findNearest(roi_shaped, k = 1)
        
        char = str(chr(int(results[0][0])))
        string += char
        rois.append(roi_resized)
        ++i

    createTrainingData(rois)
    for i in range(0, len(rois)):        
        cv2.namedWindow('roi #' + str(i), cv2.WINDOW_NORMAL)
        cv2.imshow('roi #' + str(i), rois[i])    

    return string
        
    

    
