import sys
import numpy

list = []
j = 0
all = 0
all_length = 0
allmean = []
with open(sys.argv[1],'r') as f:
	line = f.readline()
	while line:
		arr = line.strip().split()
		for i in range(len(arr)-3):
#			print i
			if arr[i+3] == "NULL":
				j += 1
				continue
			else:
#				print float(arr[i+3])
#				sum += float(arr[i+3])
				list.append(arr[i+3])
#		print list
		
		list_int = [float(i) for i in list]
#		print list_int
		summer = sum(list_int)
		all += summer
		all_length += len(list_int)
		if len(list_int) != 0:
			mean = summer/len(list_int)
			allmean.append(mean)
		else:
			mean = "null"
#			mean = sum/int(len(arr)-2-int(j))
#		list.append(str(mean))
		list = []
		line = f.readline()
#		print arr[0],summer,int(len(arr)-2-int(j)), mean
		
	print all, all_length,sum(allmean)/len(allmean)
#		print list
