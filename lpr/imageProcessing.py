# <imageProcessing.py>
# LPR Image Processing functions

# import modules
from constants import debug 
import cv2
import numpy as np

# module variables
##ref X = 0 
##ref Y = 0
##ref W = 2400
##ref H = 3200
cropX = 0 
cropY = 0
cropW = 2400
cropH = 3200

gaussianKernel = (11,11)
adaptiveThreshBlockSize = 19
adaptiveThreshWeight = 9

def cropImage(img_og):
    img = img_og.copy()
    roi = img#[cropY: cropY + cropH, cropX: cropX + cropW]

    if debug:
        print 'before crop shape: ', img.shape
        print 'after crop shape: ', roi.shape
        cv2.namedWindow('cropped image', cv2.WINDOW_NORMAL)
        cv2.imshow('cropped image', roi)

    return roi
    

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


        

        

    
