import sys
import random

##output ENSG[ensemble]	extend_start	extend_end	raw_start	raw_end	confidence
##python positiveGenerate.py input[positive.uniq] output[posive.site]
input = sys.argv[1]

output = open(sys.argv[2],'w')

d = {}
with open('/Share/home/zhangqf/sunlei/data/human/human.gene.ensemble.length','r') as length:
	line = length.readline()
	while line:
		arr = line.strip().split()
		d[arr[0]] = arr[1] 
		line = length.readline()

with open(input,'r') as f:
	line = f.readline()
	while line:
		site = line.strip().split()
		if d[site[8]] >= 100:
			if int(site[10]) - int(site[9]) <=100:
				L = int(site[10]) - int(site[9])
				start = int(site[10]) - random.randint(L,100)
				if start < 0:
					start = 0
				end = start + 100
				if end > d[site[8]]:
					end = d[site[8]]
					start = end -100
				print >> output, site[8]+'\t'+str(start)+'\t'+str(end)+'\t'+site[9]+'\t'+site[10]+'\t'+site[4]
			else:
				L = int(site[10]) - int(site[9])
				start = int(site[10]) - random.randint(100,L)
				end = start +100
				print >> output, site[8]+'\t'+str(start)+'\t'+str(end)+'\t'+site[9]+'\t'+site[10]+'\t'+site[4]
			line = f.readline()
		else:
			continue
			line = f.readline()
		
		
