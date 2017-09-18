#!/Share/home/zhangqf/usr/anaconda/bin/python

import sys
import random

input = sys.argv[1]
output = sys.argv[2]
method = sys.argv[3]
def seq2ord(seq):
	ord_list = []
	seq2ord_dict = {'A':'0', 'C':'1', 'G':'2', 'T':'3'}
	for i in range(len(seq)):
		#ord_list.append(seq2ord_dict[seq[i]])
		ord_list.append(seq[i])
	return ord_list

of = open(output, 'w')
if method == 'seq':
	with open(input, 'r') as f:
		lines = f.readlines()
		random.shuffle(lines)
		print >>of, "@RELATION seq\n"
		for i in range(len(lines[0].split('\t')[0])):
			print >>of, "@ATTRIBUTE f"+str(i+1)+" {A,C,G,T}"
		print >>of, "@ATTRIBUTE class {1,0}\n"
		print >>of, "@DATA"	
		for line in lines:
			arr = line.strip().split('\t')
			print >>of, ','.join(seq2ord(arr[3])) + "," + arr[27]
elif method == 'ch':
	with open(input, 'r') as f:
		lines = f.readlines()
		random.shuffle(lines)
		print >>of, "@RELATION icshape_invitro\n"
		for i in range(len(lines[0].split('\t')[0])*8):
			print >>of, "@ATTRIBUTE f"+str(i+1)+" numeric"
		print >>of, "@ATTRIBUTE class {1,0}\n"
		print >>of, "@DATA"	
		for line in lines:
			arr = line.strip().split('\t')
			print >>of, arr[4] + "," + arr[5]+ "," + arr[6]+ "," + arr[7]+ "," + arr[8]+ "," + arr[9]+ "," + arr[10]+ "," + arr[11]+ "," + arr[27]
elif method == 'np':
	with open(input, 'r') as f:
		lines = f.readlines()
		random.shuffle(lines)
		print >>of, "@RELATION icshape_invivo\n"
		for i in range(len(lines[0].split('\t')[0])*8):
			print >>of, "@ATTRIBUTE f"+str(i+1)+" numeric"
		print >>of, "@ATTRIBUTE class {1,0}\n"
		print >>of, "@DATA"	
		for line in lines:
			arr = line.strip().split('\t')
			print >>of,  arr[12] + "," + arr[13]+ "," + arr[14]+ "," + arr[15]+ "," + arr[16]+ "," + arr[17]+ "," + arr[18]+ "," + arr[19]+ "," + arr[27]
elif method == 'cy':
	with open(input, 'r') as f:
		lines = f.readlines()
		random.shuffle(lines)
		print >>of, "@RELATION icshape\n"
		for i in range(len(lines[0].split('\t')[0])*6):
			print >>of, "@ATTRIBUTE f"+str(i+1)+" numeric"
		print >>of, "@ATTRIBUTE class {1,0}\n"
		print >>of, "@DATA"	
		for line in lines:
			arr = line.strip().split('\t')
			print >>of,  arr[20] + "," + arr[21]+ "," + arr[22]+ "," + arr[23]+ "," + arr[24]+ "," + arr[25]+ "," + arr[27]
elif method == 'str':
        with open(input, 'r') as f:
                lines = f.readlines()
                random.shuffle(lines)
                print >>of, "@RELATION icshape\n"
                for i in range(len(lines[0].split('\t')[0])*22):
                        print >>of, "@ATTRIBUTE f"+str(i+1)+" numeric"
                print >>of, "@ATTRIBUTE class {1,0}\n"
                print >>of, "@DATA"
                for line in lines:
                        arr = line.strip().split('\t')
                        print >>of,  arr[4] + "," + arr[5]+ "," + arr[6]+ "," + arr[7]+ "," + arr[8]+ "," + arr[9]+ "," + arr[10]+ "," + arr[11]+ "," +arr[12] + "," + arr[13]+ "," + arr[14]+ "," + arr[15]+ "," + arr[16]+ "," + arr[17]+ "," + arr[18]+ "," + arr[19]+ "," + arr[20] + "," + arr[21]+ "," + arr[22]+ "," + arr[23]+ "," + arr[24]+ "," + arr[25]+ "," + arr[27]

elif method == 'combine':
	with open(input, 'r') as f:
		lines = f.readlines()
		random.shuffle(lines)
		print >>of, "@RELATION combine\n"
		for i in range(len(lines[0].split('\t')[0])*23):
			if i < len(lines[0].split('\t')[0]):
				print >>of, "@ATTRIBUTE f"+str(i+1)+" {A,C,G,T}"
			else:
				print >>of, "@ATTRIBUTE f"+str(i+1)+" numeric"
		print >>of, "@ATTRIBUTE class {1,0}\n"
		print >>of, "@DATA"	
		for line in lines:
			arr = line.strip().split('\t')
			print >>of, ','.join(seq2ord(arr[0])) + "," + arr[4] + "," + arr[5]+ "," + arr[6]+ "," + arr[7]+ "," + arr[8]+ "," + arr[9]+ "," + arr[10]+ "," + arr[11]+ "," +arr[12] + "," + arr[13]+ "," + arr[14]+ "," + arr[15]+ "," + arr[16]+ "," + arr[17]+ "," + arr[18]+ "," + arr[19]+ "," + arr[20] + "," + arr[21]+ "," + arr[22]+ "," + arr[23]+ "," + arr[24]+ "," + arr[25]+ "," + arr[27]



of.close()



