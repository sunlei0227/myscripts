#! /Share/home/zhangqf/usr/anaconda/bin/python
import sys,os

icSHAPE = sys.argv[1]
bed = sys.argv[2]
out_file = sys.argv[3]


with open(icSHAPE,'r') as file1:
	icshape_lines = file1.readlines()
	d = dict()
	for line in icshape_lines:
		icshape_data = line.strip().split("\t")
	#	print data
		d[icshape_data[0]] = icshape_data[3:]
	
#print d.keys()


mylist = []
with open(bed,'r') as file2:
	bed_lines = file2.readlines()
	for line in bed_lines:
		icshape_data = line.strip().split('\t')
		ensemble = icshape_data[6]
		start = int(icshape_data[7])
		end = int(icshape_data[8])
		mylist.append([ensemble, start, end])


with open(out_file,"w") as OUT:
	for arr in mylist:
		ensemble = arr[0]
		start = arr[1]
		end = arr[2]
		if ensemble in d.keys():
			if 'NULL' not in d[ensemble][start:end]:
				print >> OUT, d[ensemble][start:end] 
	
	



	
	
