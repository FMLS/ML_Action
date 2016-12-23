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

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat   = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h       = (dataMatrix * weights)
        error   = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error

    return weights


dataMat, labelMat = loadDataSet()

print dataMat,
print labelMat,


weights = gradAscent(dataMat, labelMat)
#print weights
