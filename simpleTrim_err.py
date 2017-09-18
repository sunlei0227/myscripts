#the print number is the patern number. we can nums*4 as the lines
H = open('Chr_D1.rmdup.fastq')
nums = 0
count = 0
line = H.readline()
while line:
	count += 1
	if count == 4:
		nums += 1
		count = 0
	if count == 1:
		if line[0] != '@':
			print nums
			break
	line = H.readline()

Line = nums*4
#sed -n 'Line-10,Line+10p' Chr_D1.rmdup.fastq2 
# To see the err line
#sed -i '4652638d' file1>file2
