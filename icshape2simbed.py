import sys

icshape = sys.argv[1]
output = open(sys.argv[2],'w')

with open(icshape,'r') as f:
	line = f.readline()
	print >>output, "track graphType=bedgraph itemRgb=on" 
	while line:
		arr = line.strip().split()
		for i in range(len(arr)-3):
			if arr[i+3] == "NULL":
				continue
			else:
				print >>output, arr[0][1:],i,i+1,arr[i+3]
		line = f.readline()
		
