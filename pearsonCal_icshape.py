from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.optimize import curve_fit
import copy



fignum = 0

def func(x, a, b, c):
    return a * np.exp(-b * x) + c



def main():
    files = [ 'ch_np_vitro.icshape.merge','ch_np_vivo.icshape.merge']
    names = [ 'ch_np_vitro', 'ch_np_vivo']
    colors = [ 'red', 'blue']
    for file, name, mycolor in zip(files, names, colors):
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
    plt.title("Correlations of RNA ch_D1")
    pltLegend = []
    for file, name, mycolor in zip(files, names, colors):
        X, Y = calPearson(file)
        accumulateX, countX = calCumuFre(X, Y)
        accumulateX.append(0)
        countX.append(1)
        h , = ax.plot(accumulateX, countX, color = mycolor, label = name, linewidth = 2)
        pltLegend.append(h)
    plt.xticks(np.linspace(-1,1,11))
    plt.yticks(np.linspace(0,1.2, 7))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    ax.legend(handles = pltLegend, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig('AllCumuFre_PearsonCorD' + sys.argv[1] + 'U' + sys.argv[2] + '.png')


def calPearson(file):
    with open(file) as f:
        lines = f.readlines()
        transcriptMap = {}
        formerData = None
        for line in lines[1:]:
            currentData = line.split('\t')
            if float(currentData[2]) < int(sys.argv[1]) or float(currentData[2]) > int(sys.argv[2]):
                formerData = None
                continue
            if formerData == None:
                formerData = currentData
                continue
            elif currentData[0] == formerData[0]:
                x = [float(a) for a in formerData[3:]]
                y = [float(a) for a in currentData[3:]]
                pearsonCor = pearsonr(x, y)
                meanDen = (float(currentData[2]) + float(formerData[2])) / 2
                transcriptMap[currentData[0]] = [meanDen, pearsonCor[0]]
                formerData = None
            else:
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
    plt.title(file)
    plt.savefig(name + 'PearsonCorD' + sys.argv[1] + 'U' + sys.argv[2] + '.png')   


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
    plt.savefig('Mean_PearsonCorD' + sys.argv[1] + 'U' + sys.argv[2] + '.png')   




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
    plt.savefig('Min_PearsonCorD' + sys.argv[1] + 'U' + sys.argv[2] + '.png')   





def calCumuFre(pX, Y):
#  calculate cumulative frequency
    X = sorted(pX, reverse=True)
    length = len(X)
    accumulateX = []
    countX = []
    currentX = X[0]
    count = 1
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
    plt.savefig('CumuFre_PearsonCorD' + sys.argv[1] + 'U' + sys.argv[2] + '.png')

main()

