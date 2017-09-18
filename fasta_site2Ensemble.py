import sys
import re

fasta = sys.argv[1]
bed = sys.argv[2]
output = open(sys.argv[3],'w')
def Readfasts(fasta):
    with open(fasta,'r') as f:
        line = f.readline()
        flag = ''
        d = {}
        seq = ''
        while line:
            if line[0] == '>':
                if flag == '':
                    ensemble = re.match(r'>(.*)(...)',line,re.I)
                    flag = ensemble.group(1)
                else:
                    d[flag] = seq
                    seq = ''
                    flag = re.match(r'>(.*)(...)',line,re.I).group(1)
            else:
                seq += line.strip()
            line = f.readline()
        d[flag] = seq
    return d
Fasta = Readfasts(fasta)

def Readbed(bed):
	with open(bed,'r') as b:
		line = b.readline()
		d = {}
		while line:
			arr = line.strip().split()
			ensemble = arr[0]+':'+arr[1]+'-'+arr[2]
			d[ensemble] = arr[3]
			line = b.readline()
	return d

Bed = Readbed(bed)

for i in Bed.keys():
	if i in Fasta.keys():
		print >> output, '>' + Bed[i]+ '\n' + Fasta[i]
	else:
		continue
output.close()
	
