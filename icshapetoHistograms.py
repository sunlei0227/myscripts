#! /usr/bin/env/python
#import numpy as np
#import pylab as pl
import sys
#from bokeh.plotting import figure, show, output_file,vplot
#import scipy.special
result=[]
file_1=open(sys.argv[1],'r')
fii=file_1.read()
print fii
fi=fii.split('	')
file_1.close()
del fi[:3]
#print fi
fi.pop()
print fi
lenfi=len(fi)
for i in range(lenfi):
    if fi[i]=='NULL':
        fi[i]=-1
    else:
        fi[i] = float(fi[i])
#    fi= str(fi)
print fi
#    result.append(fi)
#N = lenfi
#x = list(range(N))
#y = fi
#result[]
file_out = open('result','w')
file_out.write(str(fi))
file_out.close()
#output_file(sys.argv[1]+".html", title=sys.argv[1])
#pl.hist(y)
#pl.show()
#p4 = figure(title="icSHAPE histgram",tools="save",
#               background_fill="#E8DDCB")
#pl.plot(x,y)
#measured = fi
#hist, edges = np.histogram(measured, density=True, bins=60)
#p4.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
#             fill_color="#036564", line_color="#033649",\
#                     )
#p4.xaxis.axis_label = 'bp'
#p4.yaxis.axis_label = 'icSHAPE value'
#show(vplot(p4)) 
#from bokeh.charts import Dot, show, output_file

#
# build a dataset where multiple columns measure the same thing

# create a line chart where each column of measures receives a unique color and dash style
