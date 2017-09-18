import sys

input = sys.argv[1]
output = open(sys.argv[2],'w')

tag = 1
with open(input,'r') as f:
	line = f.readline()
	while line:
		arr = line.strip().split()
		if tag == 1:
			pre_end = int(arr[2])
			pre_chr = arr[0]
			tag = 0
			print >> output, '\t'.join(arr)
			line = f.readline()
		if tag == 0:
			list = arr
			now_start = int(arr[1])
			now_end = int(arr[2])
			now_chr = arr[0]
			tag = 2
			line = f.readline()
		else:
			after_start = int(arr[1])
			after_chr = arr[0]
			if now_chr == after_chr == pre_chr:
				if now_start > pre_end and now_end < after_start:
					print >> output, '\t'.join(list)
					pre_end = now_end
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2
					list = arr
					line = f.readline()
				else:
					print list
#					pre_end = int(arr[2])
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2
					list = arr
					line = f.readline()
			if now_chr != after_chr:
				if now_start > pre_end:
					print >> output, '\t'.join(list)
					pre_end = now_end
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2            
					list = arr         
					line = f.readline()
				else:
					print list         
#                   pre_end = int(arr[2])
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2            
					list = arr         
					line = f.readline()
			if now_chr != pre_chr:   
				if now_end < after_start:
					print >> output, '\t'.join(list)
					pre_end = now_end  
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2            
					list = arr         
					line = f.readline()
				else:                  
					print list         
#					pre_end = int(arr[2])
					now_start = after_start
					now_end = int(arr[2])
					now_chr = after_chr
					tag = 2            
					list = arr         
					line = f.readline()
