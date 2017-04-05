# <characterDetector>
# LPR Character Detection functions

# import modules
from constants import debug
import random
import math
import cv2
import numpy as np

# module variables
# single contour limits
cntMinArea = 45
cntMinWidth = 3
cntMinHeight = 15
cntMinRatio = 0.23
cntMaxRatio = 0.43
cntMinAngle = -15.0
cntMaxAngle = 0

# group contor limits
cntsMaxDiagonalMultiple = 10.0
cntsMaxAngleDiff = 10.0
cntsMaxAreaDiff = 0.25
cntsMaxWidthDiff = 0.25
cntsMaxHeightDiff = 1

def getContoursOfInterest(img_thresh):
    _, contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    riveting_contours = []
    
    for cnt in contours:
        if checkContourForInterest(cnt):
            riveting_contours.append(cnt)       

    if debug:
        print('interesting countors count: ' + str(len(riveting_contours)))
        height, width = img_thresh.shape       
        
        img_temp = np.zeros((height, width, 3), np.uint8)
        cv2.drawContours(img_temp, contours, -1, (255, 255, 255))
        cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
        cv2.imshow('contours', img_temp)
        
        img_temp = np.zeros((height, width, 3), np.uint8) 
        cv2.drawContours(img_temp, riveting_contours, -1, (255, 255, 255))
        cv2.namedWindow('contours of interest', cv2.WINDOW_NORMAL)
        cv2.imshow('contours of interest', img_temp)
    
    return riveting_contours


def checkContourForInterest(cnt):
    # get bounding rectangle variables of interest
    (x, y), (width, height), angle = correctBoundingRect(cv2.minAreaRect(cnt))
    area = width * height   

    if area == 0:
        return False
    
    ratio = float(width) / float(height)

    # check the variables of interest
    return (area > cntMinArea and
            width > cntMinWidth and
            height > cntMinHeight and
            ratio > cntMinRatio and
            ratio < cntMaxRatio and
            angle > cntMinAngle
            )


def groupContoursOfInterest(hw, contours):        
    groups = []

    # return an empty array
    if len(contours) == 0:
        return groups

    rnge = range(0, len(contours))
    
    # array of bounding rectangles
    rects = []
    for i in rnge:
        rects.append([contours[i], correctBoundingRect(cv2.minAreaRect(contours[i]))])

    copy = rects[:]
    
    while len(copy) > 0:
        cnt1, rect1 = copy.pop()
        group = [cnt1]
        copy2 = copy[:]

        while len(copy2) > 0:
            if len(group) > 8:
                break
            
            cnt2, rect2 = copy2.pop()
            if isMatch(rect1, rect2):
                group.append(cnt2)
                
        if len(group) > 2 and len(group) < 8:
            # add the group to the groups
            groups.append(group)

    if(len(groups) == 0):
        return None

    # return the largest group
    groups.sort(key = len, reverse = True)        
    
    if debug:
        print 'number of groups: ' + str(len(groups))
        img_temp = np.zeros((hw[0], hw[1], 3), np.uint8)
        
        for i in range(0, 1):
            rgbVal1 = 100 if random.uniform(0, 1) < 0.5 else 255
            rgbVal2 = 100 if random.uniform(0, 1) < 0.5 else 255
            rgbVal3 = 100 if random.uniform(0, 1) < 0.5 else 255
            cv2.drawContours(img_temp, groups[i], -1, (rgbVal1, rgbVal2, rgbVal3))
            
        cv2.namedWindow('groups', cv2.WINDOW_NORMAL)
        cv2.imshow('groups', img_temp)      
        
        for i in range(0, 1):
            group = groups[i]
            for j in range(0, len(group)):
                cnt = group[j]
                rect = correctBoundingRect(cv2.minAreaRect(cnt))
                box = np.int0(cv2.boxPoints(rect))
                cv2.drawContours(img_temp, [box], 0, (255, 0, 0))
            
        cv2.namedWindow('min bounding', cv2.WINDOW_NORMAL)
        cv2.imshow('min bounding', img_temp)
        cv2.imwrite('/home/pi/Pictures/min_bounding.jpg', img_temp)
    return groups[0]
    


# Checks the contours bounding rectangles to see if they match
def isMatch(rect1, rect2):
    [(x1, y1), (width1, height1), angle1] = rect1
    [(x2, y2), (width2, height2), angle2] = rect2
    
    area1 = width1 * height1
    xcenter1 = ((2 * x1) + width1) / 2
    ycenter1 = ((2 * y1) + height1) / 2
    diagonal1 = math.sqrt((width1 ** 2) + (height1 ** 2))
    
    area2 = width2 * height2
    xcenter2 = ((2 * x2) + width2) / 2
    ycenter2 = ((2 * y2) + height2) / 2
    diagonal2 = math.sqrt((width2 ** 2) + (height2 ** 2))

    # calculate the distance between the two contours
    xcenterDiff = abs(xcenter1 - xcenter2)
    ycenterDiff = abs(ycenter1 - ycenter2)
    distance = math.sqrt((xcenterDiff ** 2) + (ycenterDiff ** 2))

    # calculate the angle betwen the contours
    angleDiff = float(abs(float(angle1) - float(angle2)))

    # calculate difference in area, width, and height
    areaDiff = float(abs(area1 - area2)) / float(area1)
    widthDiff = float(abs(width1 - width2)) / float(width1)
    heightDiff = float(abs(height1 - height2)) / float(height1)

    # check calculations
    return (distance < (diagonal2 * cntsMaxDiagonalMultiple) and
            angleDiff < cntsMaxAngleDiff and
            areaDiff < cntsMaxAreaDiff and
            widthDiff < cntsMaxWidthDiff and
            heightDiff < cntsMaxHeightDiff)

def correctBoundingRect(rect):
    (x, y), (w, h), angle = rect

    if (w * h) == 0:
        return rect
    
    ratio_inv = float(h) / float(w)
    
    if ratio_inv > cntMinRatio and ratio_inv < cntMaxRatio:
        adj_angle = -(90 + angle)
        rect = ((x, y), (h, w), adj_angle)

    return rect
    
    
