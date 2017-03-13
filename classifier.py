import cv2
import numpy as np
import characterDetector as cd

kn = cv2.ml.KNearest_create()

def train():
    classifications = np.loadtxt("classifications.txt", np.float32)
    flattened = np.loadtxt("flattened_images.txt", np.float32)
    classifications = classifications.reshape((classifications.size, 1))
    kn.setDefaultK(1)
    
    kn.train(flattened, cv2.ml.ROW_SAMPLE, classifications)


def detectCharacters(thresh, group):
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)     

    string = ""
    rois = []
    i = 0
    for cnt in group:
        rect = cd.correctBoundingRect(cv2.minAreaRect(cnt))
        (x, y), (w, h), angle = rect

        roi = thresh[y - h/2 - 0 : y + h/2 + 0, x - w/2 - 0: x + w/2 + 0]
        roi_resized = cv2.resize(roi, (20, 30))
        
        roi_shaped = roi_resized.reshape((1, 20*30))
        roi_shaped = np.float32(roi_shaped)

        retval, results, resp, dists = kn.findNearest(roi_shaped, k = 1)

        char = str(chr(int(results[0][0])))
        string += char
        rois.append(roi_resized)
        ++i

    for i in range(0, len(rois)):        
        cv2.namedWindow('roi #' + str(i), cv2.WINDOW_NORMAL)
        cv2.imshow('roi #' + str(i), rois[i])    

    print(string)
    return string
        
    

    
