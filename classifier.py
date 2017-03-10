import cv2
import numpy as np
import characterDetector as cd

kn = cv2.ml.KNearest_create()

def train():
    classifications = np.loadtxt("classifications.txt", np.float32)
    flattened = np.loadtxt("flattened_images.txt", np.float32)
    classifications = classifications.reshape((classifications.size, 1))
    kn.setDefaultK(1)

    print 'cs: ', classifications.shape
    print 'flat: ', flattened.shape
    
    kn.train(flattened, cv2.ml.ROW_SAMPLE, classifications)


def detectCharacters(thresh, group):
##    h, w = thresh.shape
##    thresh_color = np.zeros((h, w, 3), np.uint8)
    #thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
      

    string = ""
    rois = []
    i = 0
    for cnt in group:
        rect = cd.correctBoundingRect(cv2.minAreaRect(cnt))
        (x, y), (w, h), angle = rect

        roi = thresh[y - h/2 - 0 : y + h/2 + 0, x - w/2 - 0: x + w/2 + 0]
        roi_resized = cv2.resize(roi, (20, 30))
        
        print 'roi shape: ', roi_resized.shape
        
        roi_shaped = roi_resized.reshape((1, 20*30))
        roi_shaped = np.float32(roi_shaped)

        print 'roi shape: ', roi_shaped.shape

        retval, results, resp, dists = kn.findNearest(roi_shaped, k = 1)
        print 'retval: ', retval

        char = str(chr(int(results[0][0])))
        string += char
        rois.append(roi_resized)
        ++i

    print 'rois: ', len(rois)
    for i in range(0, len(rois)):        
        cv2.namedWindow('colorized thresh ' + str(i), cv2.WINDOW_NORMAL)
        cv2.imshow('colorized thresh ' + str(i), rois[i])    

    print(string)
        
    

    
