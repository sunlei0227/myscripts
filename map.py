#! /Share/home/zhangqf/usr/anaconda/bin/python

import sys

bound = 10
bound = int(sys.argv[4])

def load_data(f1_content):
	data = {}
	for line in f1_content:
		linelist = line.strip().split('\t')
		chr = linelist[0]
		start = int(linelist[1]) + bound
		end = int(linelist[2]) - bound
		strand = linelist[5]
		if chr not in data.keys():
			#data[chr] = [];
			data[chr] = {};
			data[chr]["-"] = [];
			data[chr]["+"] = [];
		data[chr][strand].append([start, end])
		#data[chr].append([start, end])
	return data

def binary_search(start,end,chr_list):
	if(len(chr_list) == 0):
		 return [];
	minVal = 0
	maxVal = len(chr_list) - 1
	while 1:
		if  maxVal-1 <= minVal:
			print "maxVal:",maxVal,"minVal:",minVal
			break
		m = (minVal + maxVal) // 2
	#	print m,"chr_list",chr_list[m][0],"start",start,"end",end
		if chr_list[m][0] < start:
			minVal = m 
		elif chr_list[m][0] > start:
			maxVal = m 
		else:
			minVal = maxVal = m
			break
	index = minVal;
	result_list = []
	if index < len(chr_list)-1:
		print "chr_list[",index+1,"]",chr_list[index+1],"\n"
	while index < len(chr_list) and chr_list[index][1] <= end:
		if chr_list[index][0] >= start:
			result_list.append(index)
		index += 1
	return result_list
		
		


bedfile = sys.argv[1]
icshapefile = sys.argv[2]
bedsh_map = sys.argv[3]
f1 = open(bedfile,'r')
f2 = open(icshapefile,'r')
f3 = open(bedsh_map,"w")
f1_content = f1.readlines()
f2_content = f2.readlines()

bed_data = load_data(f1_content)

for line in f2_content[1:]:
        linelist = line.strip().split('\t')
	if len(linelist[0]) < 4:
		linelist[0] = "chr" + linelist[0]
        ichr = linelist[0]
        istart = int(linelist[1])
        iend = int(linelist[2])
	iseq = linelist[3]
	ivalue = linelist[4].split(',')
	istrand = linelist[5]
	try:
		indexList = binary_search(istart,iend,bed_data[ichr][istrand])
		#index = binary_search(istart,iend,bed_data[ichr])
	except KeyError:
		print "ichr",ichr, " istrand", istrand, " no match chr or strand"
		continue
		
	if len(indexList) > 0:
		print "index:",indexList
		for index in indexList:
			start_bed = int(bed_data[ichr][istrand][index][0])
			end_bed = int(bed_data[ichr][istrand][index][1])
			s1 = start_bed - istart
			s2 = iend - end_bed
			if istrand == "+":
				if s2 == 0:
					newline = [ichr,str(start_bed),str(end_bed),iseq[s1:],','.join(ivalue[s1:])]	
				else:
					newline = [ichr,str(start_bed),str(end_bed),iseq[s1:-s2],','.join(ivalue[s1:-s2])]
				#print iseq[s1:-s2]
			else:
				if s1 == 0:
					newline = [ichr,str(start_bed),str(end_bed),iseq[s2:],','.join(ivalue[s2:])]	
				else:
					newline = [ichr,str(start_bed),str(end_bed),iseq[s2:-s1],','.join(ivalue[s2:-s1])]
				#print iseq[s2:-s1]
			print "map bed start and end site to icshape seq"
			print ichr,"start:end bed",start_bed,end_bed,"start:end icshape",istart,iend
  			print >> f3, '\t'.join(newline)

''' for line in f1_content:
                linelist = line.strip().split('\t')
                chr_bed = linelist[0]
                start_bed = int(linelist[1])
                end_bed = int(linelist[2])
                if chr_bed == ichr:
                        if (start >= istart) & (end <= iend):
                                newline[1] = str(start)
                                newline[2] = str(end)
                                print "map bed start and end site to icshape seq"
                                print chr_bed,"start:end bed",start,end,ichr,"start:end icshape",istart,iend
                          #      s1 = start - istart              #s1 for slice seq start
                           #     s2 = iend - end                  #s2 for slice seq end
                                newline = [chr_bed,start,end,iseq[s1:-s2],ivalue[s1*2:-s2*2],"+"]
			#	newline[3] = iseq[s1:-s2]
                         #       newline[4] = ivalue[s1*2:-s2*2]
                                newline.append("+")
                                print >> f3, '\t'.join(linelist)
'''
f1.close()
f2.close()
f3.close()

