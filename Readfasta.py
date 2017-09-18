import sys
import re

fasta = sys.argv[1]
output = open(sys.argv[2],'w')
def Readfasts(fasta):
        with open(fasta,'r') as f:
                line = f.readline()
                flag = ''
                d = {}
                seq = ''
                while line:
                        if line[0] == '>':
                                if flag == '':
                                        ensemble = re.match(r'>(.*)',line,re.I)
                                        flag = ensemble.group(1)
                                else:
                                        if '_' in flag:
                                                seq = ''
                                                flag = re.match(r'>(.*)',line,re.I).group(1)
                                        else:
                                                d[flag] = seq
                                                seq = ''
                                                flag = re.match(r'>(.*)',line,re.I).group(1)
                        else:
                                seq += line.strip()
                        line = f.readline()
                d[flag] = seq
        return d
d = Readfasts(fasta)
for k in d.keys():
	if k[0:5]=='chrMT':
		print >>output, '>'+k+'\n'+d[k]
