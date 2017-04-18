# <characterDetector>
# LPR Character Detection functions

# import modules
from constants import debug
import random
import math
import cv2
import numpy as np
from contour import *

# module variables
# single contour limits
##cntMinArea = 45
##cntMinWidth = 3
##cntMinHeight = 15
##cntMinRatio = 0.23
##cntMaxRatio = 0.43
##cntMinAngle = -15.0
##cntMaxAngle = 0
cntMinArea = 45
cntMinWidth = 3
cntMinHeight = 15
cntMinRatio = 0.23 # W/H
cntMaxRatio = 0.43 # W/H
cntMinAngle = -90.0
cntMaxAngle = 0

# group contor limits
##cntsMaxDiagonalMultiple = 10.0
##cntsMaxAngleDiff = 10.0
##cntsMaxAreaDiff = 0.25
##cntsMaxWidthDiff = 0.25
##cntsMaxHeightDiff = 1
##cntsMaxDiagonalMultiple = 5.0
##cntsMaxAngleDiff = 45.0
##cntsMaxAreaDiff = 0.45
##cntsMaxWidthDiff = 0.45
##cntsMaxHeightDiff = 0.2
##groupMinSlopeDiff = 0.0
##groupMaxSlopeDiff = 0.1
cntsMaxDiagonalMultiple = 5.0
cntsMaxAngleDiff = 50.0
cntsMaxAreaDiff = 0.25
cntsMaxWidthDiff = 0.25
cntsMaxHeightDiff = 1
groupMinSlopeDiff = 0.0
groupMaxSlopeDiff = 0.1

def getContoursOfInterest(img_thresh):
    _, contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    riveting_contours = []
    
    for cnt in contours:
        old_rect = cv2.minAreaRect(cnt)
        rect = correctBoundingRect(old_rect)
        if checkContourForInterest(cnt, rect):
            riveting_contours.append(Contour(cnt, rect))       

    if debug:
        print('interesting countors count: ' + str(len(riveting_contours)))
        height, width = img_thresh.shape       
        
        img_temp = np.zeros((height, width, 3), np.uint8)
        cv2.drawContours(img_temp, contours, -1, (255, 255, 255))        
        cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
        cv2.imshow('contours', img_temp)
        
        img_temp = np.zeros((height, width, 3), np.uint8) 
        for i in range(0, len(riveting_contours)):            
            cv2.drawContours(img_temp, riveting_contours[i].cnt, -1, (255, 255, 255))
            
        cv2.namedWindow('contours of interest', cv2.WINDOW_NORMAL)
        cv2.imshow('contours of interest', img_temp)
    
    return riveting_contours


def checkContourForInterest(cnt, rect):
    # get bounding rectangle variables of interest
    (x, y), (width, height), angle = rect
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


# Caclulates the average slope of the group
def calcAvgSlope(group):
    slopes = []
    # the first contour bounding box is what we calc slope against
    (x1, y1), (width1, height1), angle1 = group[0].rect 
    xcenter1 = ((2 * x1) + width1) / 2
    ycenter1 = ((2 * y1) + height1) / 2

    # loop through the other members of the group, calculating the slope
    for i in range(1, len(group)):
        (x2, y2), (width2, height2), angle2 = group[i].rect      
        xcenter2 = ((2 * x2) + width2) / 2
        ycenter2 = ((2 * y2) + height2) / 2
        slopes.append((ycenter2 - ycenter1) / (xcenter2 - xcenter1))

    # return the average of the slopes
    return np.average(slopes)        


def groupContoursOfInterest(hw, contours):        
    groups = []

    # return an empty array
    if len(contours) == 0:
        return groups

    # loop through the list of contours
    for cnt1 in contours:
        group = [cnt1]
        slope = 0

        # loop through the list of contours again    
        for cnt2 in contours:
            
            # group is too large, break
            if len(group) > 9:
                break

            # match the contour from the first loop with the contour from the second loop
            if isMatch(cnt1.rect, cnt2.rect, slope):
                group.append(cnt2)
                
                # recalc the slope
                slope = calcAvgSlope(group)

        # add the group to the groups
        if len(group) > 2 and len(group) < 9:
            groups.append(group)

    if len(groups) == 0:
        return None

    # sort by largest individual group size first
    groups.sort(key = len, reverse = True)

    #### Debug
    if debug:
        print 'number of groups: ' + str(len(groups))
        img_temp = np.zeros((hw[0], hw[1], 3), np.uint8)
        
        for i in range(0, 1):
            rgbVal1 = 100 if random.uniform(0, 1) < 0.5 else 255
            rgbVal2 = 100 if random.uniform(0, 1) < 0.5 else 255
            rgbVal3 = 100 if random.uniform(0, 1) < 0.5 else 255
            for j in range(0, len(groups)):
                for g in range(0, len(groups[j])):                    
                    cv2.drawContours(img_temp, groups[j][g].cnt, -1, (rgbVal1, rgbVal2, rgbVal3))
            
        cv2.namedWindow('groups', cv2.WINDOW_NORMAL)
        cv2.imshow('groups', img_temp)      
        
        for i in range(0, 1):
            group = groups[i]
            for j in range(0, len(group)):
                cnt = group[j]
                box = np.int0(cv2.boxPoints(cnt.rect))
                cv2.drawContours(img_temp, [box], 0, (255, 0, 0))
            
        cv2.namedWindow('min bounding', cv2.WINDOW_NORMAL)
        cv2.imshow('min bounding', img_temp)
        cv2.imwrite('/home/pi/Pictures/min_bounding.jpg', img_temp)
    #### Debug        

    # return largest group
    return groups[0]

            
    
##
##    copy = contours[:]
##    
##    while len(copy) > 0:
##        contour1 = copy.pop()
##        group = [contour1]
##        
##        copy2 = copy[:]
##
##        while len(copy2) > 0:
##            if len(group) > 9:
##                break
##            
##            contour2 = copy2.pop()
##            if isMatch(contour1.rect, contour2.rect):
##                group.append(contour2)
##                
##        if len(group) > 2 and len(group) < 9:
##            # add the group to the groups
##            groups.append(group)
##
##    if len(groups) == 0:
##        return None
##
##    # return the largest group
##    groups.sort(key = len, reverse = True)
##    
##    if debug:
##        print 'number of groups: ' + str(len(groups))
##        img_temp = np.zeros((hw[0], hw[1], 3), np.uint8)
##        
##        for i in range(0, 1):
##            rgbVal1 = 100 if random.uniform(0, 1) < 0.5 else 255
##            rgbVal2 = 100 if random.uniform(0, 1) < 0.5 else 255
##            rgbVal3 = 100 if random.uniform(0, 1) < 0.5 else 255
##            for j in range(0, len(groups)):
##                for g in range(0, len(groups[j])):                    
##                    cv2.drawContours(img_temp, groups[j][g].cnt, -1, (rgbVal1, rgbVal2, rgbVal3))
##            
##        cv2.namedWindow('groups', cv2.WINDOW_NORMAL)
##        cv2.imshow('groups', img_temp)      
##        
##        for i in range(0, 1):
##            group = groups[i]
##            for j in range(0, len(group)):
##                cnt = group[j]
##                box = np.int0(cv2.boxPoints(cnt.rect))
##                cv2.drawContours(img_temp, [box], 0, (255, 0, 0))
##            
##        cv2.namedWindow('min bounding', cv2.WINDOW_NORMAL)
##        cv2.imshow('min bounding', img_temp)
##        cv2.imwrite('/home/pi/Pictures/min_bounding.jpg', img_temp)
##        
##    return groups[0]
##    


# Checks the contours bounding rectangles to see if they match
def isMatch(rect1, rect2, avgSlope):
    [(x1, y1), (width1, height1), angle1] = rect1
    [(x2, y2), (width2, height2), angle2] = rect2

    # don't match the same contours
    if x1 == x2 and y1 == y2:
        return False
    
    area1 = width1 * height1
    xcenter1 = ((2 * x1) + width1) / 2
    ycenter1 = ((2 * y1) + height1) / 2
    diagonal1 = math.sqrt((width1 ** 2) + (height1 ** 2))
    
    area2 = width2 * height2
    xcenter2 = ((2 * x2) + width2) / 2
    ycenter2 = ((2 * y2) + height2) / 2
    diagonal2 = math.sqrt((width2 ** 2) + (height2 ** 2))

    # calculate the slope between the two center points
    den = (xcenter2 - xcenter1)
    if den == 0:
        slope = 0
    else:
        slope = (ycenter2 - ycenter1) / den
        
    if slope == 0:
        slopeDiff = 0
    else:
        slopeDiff = float(abs(slope - avgSlope))

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
            heightDiff < cntsMaxHeightDiff and
            slopeDiff > groupMinSlopeDiff and
            slopeDiff < groupMaxSlopeDiff)


# Fixes the upside down minimum bounding rectangles
def correctBoundingRect(rect):
    (x, y), (w, h), angle = rect

    if (w * h) == 0:
        return rect

    # get the ratio (WxH)
    ratio = float(w) / float(h)

    # get the inverted ratio (HxW)
    ratio_inv = float(h) / float(w)

    # if the ratio is not within the criteria but the inverted ratio is
    # then take the inverted ratio with an adjusted angle
    if (ratio < cntMinRatio or ratio > cntMinRatio) and (ratio_inv > cntMinRatio and ratio_inv < cntMaxRatio):
        adj_angle = -(90 + angle)
        rect = ((x, y), (h, w), adj_angle)

    return rect
    
    
