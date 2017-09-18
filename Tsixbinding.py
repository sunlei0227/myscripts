
import sys

input = sys.argv[1]
#/Share/home/zhangqf/sunlei/data/RBP/human2/allprotein/allprotein_hg38.bed
#output = open(sys.argv[2],'w')

#def readRepA(RepA):
with open('/Share/home/zhangqf/sunlei/data/RBP/human2/allprotein/xist_RepA_protein','r') as f:
	lines = f.readlines()
	d = []
	for line in lines:
		d.append(line.strip())
#return d
print d		

for i in range(300):
	i = i+1
	with open(input,'r') as f:
		l = []
		line = f.readline()
		a =73826200 + 5*i
		b =73826300 + 5*i
		while line:
			arr = line.strip().split()
#		for i in range(20):
#			i = i+1
#			a =  73820000+500*i
#			print arr
			if arr[0] == 'chrX' and int(arr[1]) > a and int(arr[2]) < b and arr[5] == '+':
				l.append(arr[3])
				line = f.readline()
			else:
#				continue
				line = f.readline()
#		print l
		overlap = list(set(l).intersection(set(d)))
		if len(overlap) == 0:
			print  str(len(l))+'\t'+str(len(list(set(l))))+'\t'+str(len(overlap))+'\t'+str(0)
		else:
			print str(len(l))+'\t'+str(len(list(set(l))))+'\t'+str(len(overlap))+'\t'+ str(float(len(overlap))/float(len(list(set(l)))))
				 
				
