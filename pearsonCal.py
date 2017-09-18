from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.optimize import curve_fit
import copy
from random import random
import pdb
import math



fignum = 0
down = '0'
upper = '10000'

def func(x, a, b, c):
    return a * np.exp(-b * x) + c



def main():
    files = [ x for x in sys.argv[1:] ]
    #names = [ 'D1-N1', 'D1-T1', 'T1-T2', 'D1-D2', 'N1-N2']
    names = [ x.split('.')[0] for x in files ]
    COLORS = ('red', 'blue', 'black', 'green', 'yellow')
    colors = [ COLORS[i] for i in range(len(names)) ]
    #colors = [ (random(), random(),random()) for x in files]
    for file, name, mycolor in zip(files, names, colors):
	#pdb.set_trace()
	X, Y = calPearson(file)
        drawPearson(X, Y, file, name)
    calCumuAll(files, names, colors)
    #X, Y = calPearson(files[4])
    #accumulateX, countX = calCumuFre(X, Y)
    #drawCumuFre(accumulateX, countX)


def calCumuAll(files, names, colors):
    global fignum
    fignum += 1
    plt.figure(fignum, figsize=(15,10))
    #plt.figure(1)
    ax = plt.subplot(111)
    plt.xlabel('Pearson Correlation')
    plt.ylabel('Cumulative Frequency')
    plt.title("Correlations of RNA ")
    pltLegend = []
    for file, name, mycolor in zip(files, names, colors):
        X, Y = calPearson(file)
        accumulateX, countX = calCumuFre(X, Y)
        accumulateX.append(-1.0)
        countX.append(1)
        h , = ax.plot(accumulateX, countX, color = mycolor, label = name, linewidth = 2)
        pltLegend.append(h)
    plt.xticks(np.linspace(-1,1,11))
    plt.yticks(np.linspace(0,1.2, 7))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    ax.legend(handles = pltLegend, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig('AllCumuFre_PearsonCorD' + down + 'U' + upper + '.png')


def calPearson(file):
    with open(file) as f:
        lines = f.readlines()
        transcriptMap = {}
        formerData = None
        for line in lines[1:]:
            currentData = line.strip().split('\t')
            if float(currentData[2]) < int(down) or float(currentData[2]) > int(upper):
                formerData = None
                continue
            if formerData != None and currentData[0] == formerData[0]:
                #x = [float(a) if a != 'NULL' else 0.0 for a in formerData[3:]]
                #y = [float(a) if a != 'NULL' else 0.0 for a in currentData[3:]]
		x = []
		y = []
		for index in range(len(formerData[3:])):
			if formerData[index+3] != 'NULL' and currentData[index+3] != 'NULL':
				x.append(float(formerData[index+3]))
				y.append(float(currentData[index+3]))
		if len(x) == 0:
			continue
                pearsonCor = pearsonr(x, y)
		if math.isnan(pearsonCor[0]):
			formerData = None
			continue
                meanDen = (float(currentData[2]) + float(formerData[2])) / 2
                transcriptMap[currentData[0]] = [meanDen, pearsonCor[0]]
                formerData = None
            else:
                formerData = currentData
                continue

            
    X = []
    Y = []
    for (d,x) in transcriptMap.items():
        Y.append(x[0]);
        X.append(x[1]);
    return X, Y

def drawPearson(X, Y, file, name):
    global fignum
    fignum += 1
    plt.figure(fignum) 
    plt.scatter(X, Y)
    plt.xlabel('Pearson Correlation')
    plt.ylabel('RPKM')
    plt.xticks(np.linspace(-1.2,1.2,13))
    plt.title(file)
    plt.savefig(name + 'PearsonCorD' + down + 'U' + upper + '.png')   


#calculate mean of X for each Y
def calMeanXofY(X, Y):
    zipData = zip(Y, X)
    zipData.sort()
    meanX = []
    meanY = []
    currentY = None
    xSum = 0
    xCount = 0

    for (y, x) in zipData:
        if currentY == None:
            currentY = int(y)
            xSum += x
            xCount += 1
        else:
            if (y - currentY) < 1:
                xSum += x
                xCount += 1
            else:
                meanX.append(xSum / float(xCount))
                meanY.append(currentY)
                currentY = int(y)
                xSum = x
                xCount = 1
    return meanX, meanY

def drawMeanXofY(meanX, meanY):
    plt.figure(2) 
    plt.scatter(meanX, meanY)
    plt.xlabel('Pearson Correlation')
    plt.ylabel('RPKM')
    plt.savefig('Mean_PearsonCorD' + down + 'U' + upper + '.png')   




#calculate min of X for each Y
def calMinXofY(X, Y):
    zipData = zip(Y, X)
    zipData.sort()
    minX = []
    minY = []
    currentY = None
    xMin = 0

    for (y, x) in zipData:
        if currentY == None:
            currentY = int(y)
            xMin = x
        else:
            if (y - currentY) < 10:
                xMin = min(xMin, x)
            else:
                minX.append(xMin)
                minY.append(currentY)
                currentY = int(y)
                xMin = x
    return minX, minY

def drawMinXofY(minX, minY):
    print minX
    print minY
    popt, pcov = curve_fit(func, np.array(minX), np.array(minY), bounds=(0, [3., 2., 1.]))
    plt.figure(3) 
    plt.scatter(minX, minY)
    print popt
    plt.xlabel('Pearson Correlation')
    plt.ylabel('RPKM')
    plt.savefig('Min_PearsonCorD' + down + 'U' + upper + '.png')   





def calCumuFre(pX, Y):
#  calculate cumulative frequency
    X = sorted(pX, reverse=True)
    length = len(X)
    accumulateX = []
    countX = []
    currentX = X[0]
    count = 1
    #pdb.set_trace()
    for x in X[1:]:
        if abs(x - currentX) < 0.0001:
            count += 1
        else:
            accumulateX.append(currentX)
            countX.append(float(count) / length)
            currentX = x
            count += 1
    accumulateX.append(currentX)
    countX.append(float(count) / length)
    return accumulateX, countX

def drawCumuFre(accumulateX, countX):
    global fignum
    fignum += 1
    accumulateX.append(0)
    countX.append(1)
    plt.figure(fignum) 
    #plt.scatter(meanX, meanY)
    plt.plot(accumulateX, countX)
    plt.xlabel('Pearson Correlation')
    plt.ylabel('Cumulative Frequency')
    plt.xticks(np.linspace(-1,1,11)) 
    plt.yticks(np.linspace(0,1.2, 7))
    plt.title("Correlations of RNA ch_D1")
    plt.savefig('CumuFre_PearsonCorD' + down + 'U' + upper + '.png')

main()
