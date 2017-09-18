H = open('Chr_D1.rmdup.fastq')
O = open('Chr_D1.rmdup.fastq22','w')
nums = 0
count = 0
mstr = ''
error = list()
line = H.readline()
while line:
	count += 1
	if count == 4:
		nums += 1
		count = 0
	if count == 1:
		O.writelines(mstr)
		mstr = ''
		if line[0] != '@':
			error.append(nums)
			while line[0] != '@': line = H.readline()
			count = 1
	mstr += line
	line = H.readline()

O.writelines(mstr)
O.close()


#if the file don't have the standard fastq, we find the err line and delete the pattern no matter it is 3 or 5 line
