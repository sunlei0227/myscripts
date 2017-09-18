
import sys

input = sys.argv[1]
output = open(sys.argv[2],'w')

#def Readfile(input):
with open(input,'r') as f:
	line = f.readline()
	tag =1
	pre_end = 0
	while line:
		arr = line.strip().split()
		if arr[4] != "lincRNA" and arr[4] != "sense_intronic" and arr[4] != "3prime_overlapping_ncrna" and arr[4] != "bidirectional_promoter_lncrna" and arr[4] != "macro_lncRNA" and arr[4] != "antisense" and arr[4] != "sense_overlapping" and arr[4] != "processed_transcript":
			if arr[1] < pre_end and arr[2] < pre_end:
				print >>output, '\t'.join(arr)
				line = f.readline()
			else:
				line = f.readline()
		else:
			pre_end = arr[2]
			line = f.readline()
output.close()
