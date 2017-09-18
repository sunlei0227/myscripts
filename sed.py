#! usr/bin/env python

import os

file = open("/Share/home/zhangqf/sunlei/data/RBP/human2/Sunlei_need_all_clipdb_protein_motifs/Sunlei_need_protein_info.lst",'r')
lines = file.readlines()
d = dict()

for line in lines:
	eachline = line.strip("\n").split("\t")
	d[eachline[-1]] = eachline[1]
	print eachline
	print eachline[-1]
rootpath = "/Share/home/zhangqf/sunlei/data/RBP/human2/Sunlei_need_all_clipdb_protein_motifs/cutoff_0.001"
lsts = os.listdir(rootpath)
print lsts
for lst in lsts:
	os.system( "mv " +rootpath + '/' + lst + ' ' + rootpath + '/' + d[ lst[0:3] ] )

