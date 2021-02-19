import cv2

import os
import sys
import numpy as np
import pandas as pd

#print("Open CV", cv2.__version__)


def clearGrid(data):
    x, y = data.shape
    for j in range(y-1):
        for i in range(x-1):
            switch = 0
            if data[i][j] != 255:
                switch += 1
            if data[i][j+1] != 255:
                switch += 1
            if data[i+1][j] != 255:
                switch += 1
            if data[i+1][j+1] != 255:
                switch += 1
            if switch == 1:
                if data[i][j] != 255:
                    data[i][j] = 255
                if data[i][j+1] != 255:
                    data[i][j+1] = 255
                if data[i+1][j] != 255:
                    data[i+1][j] = 255
                if data[i+1][j+1] != 255:
                    data[i+1][j+1] = 255


def isMax(markers):
    a, b = np.unique(markers, return_counts=True)
    label, pxiel = 0, 0
    for i in range(1, len(a)):
        if b[i] >= pxiel:
            pxiel = b[i]
            label = a[i]
    return label, pxiel


def getPos(markers, label):
    pos = []
    X, Y = markers.shape
    # point 1
    for y in range(Y):
        for x in range(X):
            if markers[y][x] == label:
                pos.append([x, y])
                break
        if len(pos) == 1:
            break
    # point 2
    for x in range(pos[0][0], X):
        if markers[pos[0][1]][x] == 0:
            pos.append([x-1, pos[0][1]])
            break
        if x == X-1:
            pos.append([x, pos[0][1]])
    # point 3
    for y in range(pos[0][1], Y):
        if markers[y][pos[0][0]] == 0:
            pos.append([pos[0][0], y-1])
            break
        if y == Y-1:
            pos.append([pos[0][0], y])
    # point 4
    for x in range(pos[2][0], X):
        if markers[pos[2][1]][x] == 0:
            pos.append([x-1, pos[2][1]])
            break
        if x == X-1:
            pos.append([x, pos[2][1]])
    return pos


def getEffectivePoint(markers):
    EffectivePointList = []
    for label in range(1, len(np.unique(markers, return_counts=True)[0])):
        posList = getPos(markers, label)
        for pos in posList:
            if pos[0] != 0 and pos[1] != 0:
                EffectivePointList.append(pos)

    return EffectivePointList


def featureMap(List, mapRange=[10, 10]):
    featureMap = []
    index = len(List)
    for colIndex in range(index):
        littleMap = []
        for rowIndex in range(index):
            if colIndex == rowIndex:
                continue
            if abs(List[colIndex][0] - List[rowIndex][0]) <= mapRange[0] and abs(List[colIndex][1] - List[rowIndex][1]) <= mapRange[1]:
                x = List[colIndex][0] - List[rowIndex][0]
                y = List[colIndex][1] - List[rowIndex][1]
                littleMap.append([x, y])
        if len(littleMap) == 0:
            littleMap.append([0, 0])
        featureMap.append(littleMap)
    return featureMap


def matchPoint(pointList1, pointList2):
    matchList = []

    featureMap1 = featureMap(pointList1)
    featureMap2 = featureMap(pointList2)

    for A in range(len(featureMap1)):
        for B in range(len(featureMap2)):
            count = 0
            if len(featureMap1[A]) != len(featureMap2[B]):
                continue
            for i in range(len(featureMap1[A])):
                for j in range(len(featureMap2[B])):
                    if (abs(featureMap1[A][i][0] - featureMap2[B][j][0]) <= 1) and (abs(featureMap1[A][i][1] - featureMap2[B][j][1]) <= 1):
                        count += 1
                        break
            if (abs(len(featureMap1[A]) - count) == 0):
                matchList.append([pointList1[A], pointList2[B]])
                break
    return matchList


def pxielDistance(matchList):
    dist = []
    for i in range(len(matchList)):
        x = matchList[i][1][0] - matchList[i][0][0]
        y = matchList[i][1][1] - matchList[i][0][1]
        dist.append([x, y])

    result = pd.value_counts(dist)

    if result.max() == 1 or matchList == []:
        return "unknow"
    else:
        return result.idxmax()


def birckCount(markers1, markers2):
    effectivePointList1 = getEffectivePoint(markers1)
    effectivePointList2 = getEffectivePoint(markers2)
    matchList = matchPoint(effectivePointList1, effectivePointList2)
    return pxielDistance(matchList)


def cutImage(img):
    y, x, _ = img.shape
    center_y = int(y/2)
    center_x = int(x/2)
    return img[(center_y+290):(center_y+400), (center_x-55):(center_x+55)]


def label(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_G = cv2.GaussianBlur(gray, (5, 5), 0)
    bin_img = cv2.adaptiveThreshold(
        img_G, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)

    kernel = np.ones((3, 3), np.uint8)
    next_img = cv2.erode(bin_img, kernel, iterations=2)
    if clear:
        for i in range(50):
            clearGrid(next_img)

    next_img = next_img[25:85, 25:85]

    sure_bg = cv2.dilate(next_img, kernel, iterations=2)
    dist_transform = cv2.distanceTransform(next_img, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(
        dist_transform, 0.01*dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    return markers


if __name__ == "__main__":
    # memo:
    #   input: currentImage oldImage
    #   currentImage -> oldImage
    #   output: [x,y]
    currentImageFile = "img/currentImage.png"
    oldImageFile = "img/oldImage.png"

    currentImage = cv2.imread(currentImageFile)
    oldImage = cv2.imread(oldImageFile)

    if(os.path.isfile(currentImageFile) == False):
        print("Read currentImage is Faild!")
        sys.exit(1)
    if(os.path.isfile(oldImageFile) == False):
        print("Read oldImage is Faild!")
        sys.exit(1)

    currentImage = cutImage(currentImage)
    oldImage = cutImage(oldImage)

    currentMarkers = label(currentImage)
    oldMarkers = label(oldImage)
    distance = birckCount(oldMarkers, currentMarkers)

    os.remove(oldImageFile)
    os.rename(currentImageFile, oldImageFile)
    print(distance)
