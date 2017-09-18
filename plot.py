#!/Share/home/zhangqf/usr/anaconda/bin/python

import numpy as np
import pylab as plt
import sys


input = sys.argv[1]
x = []
y1 = []
y2 = []
with open(input,'r') as f:
	lines = f.readlines()
	for line in lines:
		site = line.strip().split()
		x.append(int(site[0]))
#		print line[0],line[1],x
		y1.append(int(site[1]))
		y2.append(int(site[2]))
#		x.append(int(lines[0]))
#		y1.append(int(lines[1]))
#		y2.append(int(lines[2]))		
#		print line[0], line[2]
print x,y1,y2
#try:
 #       list1 = map(float, x)
  #      list2 = map(float, y1)
#pl.plot(x, y2)
#pl.show()

plt.figure(figsize=(8,4))
plt.plot(x,y1,label="$lable11$",color="red",linewidth=2)
plt.plot(x,y2,label="$lablel2$",color="blue",linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Your own name")
plt.ylim(1,10)
plt.legend()
plt.show()
