#! /usr/bin/env/python
import sys
file_1=open(sys.argv[1],'r')
fi=file_1.read()
file_1.close()
file_2=open(sys.argv[2],'r')
fs=file_2.read()
file_2.close()
lenfi=len(fi)
fi=fi[:lenfi-1]
lenfs=len(fs)
fs=fs[:lenfs]
gi=fi.split('	')
gs=fs.split('	')
#gi.pop(0)
#gi.pop(0)
#gi.pop(0)
#gs.pop(0)
#gs.pop(0)
lengi=len(gi)
gi.pop(lengi-1)
lengi=len(gi)
print lengi
lengs=len(gs)
gs.pop(lengs-1)
lengs=len(gs)
print lengs
#print gi
#print gs
for i in range(lengi):
#    if gi[i]=='NULL':
#        gi[i] = -1
#    else:
        gi[i] = float(gi[i])
for i in range(lengs):
    gs[i] = float(gs[i])

#print gi
#print gs
lengi=len(gi)
lengs=len(gs)
print lengi
print lengs
#gs.pop(956)
#gs.pop(955)
lengs=len(gs)
print lengs
print lengi
import numpy as np

from bokeh.plotting import figure, show, output_file, vplot

N = 956

x = list(range(N))
y = gi
z = gs

output_file(sys.argv[1]+sys.argv[2]+".html", title=sys.argv[1]+sys.argv[2])

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

p1 = figure(title=sys.argv[1], tools=TOOLS,width=1500, height=600)

p1.circle(x, y, legend=sys.argv[1])
p1.circle(x, z, legend=sys.argv[2], color="orange", )

show(vplot(p1))
