#!/usr/bin/python
from numpy import *

def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append([int(lineArr[2])])
    return dataMat, labelMat

dataMat, labelMat = loadDataSet()
print dataMat, '\n'
print labelMat,
