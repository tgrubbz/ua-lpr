# <imageProcessing.py>
# LPR Image Processing functions

# import modules
from constants import debug 
import cv2
import numpy as np

# module variables
gaussianKernel = (11,11)
adaptiveThreshBlockSize = 19
adaptiveThreshWeight = 9

def getImageThreshold(img_scene):
    img_gry = cv2.cvtColor(img_scene, cv2.COLOR_BGR2GRAY)
    img_improved_contrast = cv2.equalizeHist(img_gry)
    img_blurred = cv2.GaussianBlur(img_improved_contrast, gaussianKernel, 0)
    img_thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, adaptiveThreshBlockSize, adaptiveThreshWeight)    
    
    if debug:
        cv2.namedWindow('img_gry', cv2.WINDOW_NORMAL)
        cv2.imshow('img_gry', img_gry)
        cv2.namedWindow('img_improved_contrast', cv2.WINDOW_NORMAL)
        cv2.imshow('img_improved_contrast', img_improved_contrast)
        cv2.namedWindow('img_blurred', cv2.WINDOW_NORMAL)
        cv2.imshow('img_blurred', img_blurred)
        cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
        cv2.imshow('img_thresh', img_thresh)

    return img_thresh


        

        

    
