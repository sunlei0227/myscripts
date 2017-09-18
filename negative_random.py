import sys
import random

gene_ensemble_length = sys.argv[1]
positivebed = sys.argv[2]
negativebed = open(sys.argv[3],'w')
length = 100
d = {}
with open(gene_ensemble_length,'r') as f:
	lines = f.readlines()
	for line in lines:
		arr = line.strip().split()
		d[arr[0]] = arr[1]

with open(positivebed,'r') as p:
	line = p.readline()
	while line:
		l = line.strip().split('\t')
#		print l
		if d[l[8]] >length:
			start = random.randint(0,int(d[l[8]])-length)
			end = start + length
			print >>negativebed, '\t'.join(l[0:8])+"\t"+l[8]+"\t"+str(start)+"\t"+str(end)
		else:
			continue
		line = p.readline()
negativebed.close()
