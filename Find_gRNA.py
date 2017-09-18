import sys
import re

## python Find_gRNA.py /Share/home/zhangqf8/sunlei/data/ATAC/ourdata/gap ~/sunlei/data/human/chrMT.fa /Share/home/zhangqf8/sunlei/data/ATAC/ourdata/output

output =  open(sys.argv[3],'w')
#H = open('/Share/home/zhangqf8/sunlei/data/ATAC/ourdata/gap_200','ri')
def loadfile(f):
	choice = []
	fr = open(f)
	for line in fr.readlines():
		lineArr = line.strip().split()
		if int(lineArr[2]) > 200:
			choice.append(lineArr)
	return choice
#sl = loadfile(sys.argv[1])
#print sl,len(sl)

def loadMT(MT):
	seq = ''
	MT = open(MT)
	for line in MT.readlines():
		if line[0] == '>':
			continue
		else:
			seq += line
	return seq

#print loadMT(sys.argv[1])

choice = loadfile(sys.argv[1])
seq = loadMT(sys.argv[2])

## this can find the sequence, but we should find the sites first
#for site in choice:
#	choice_site =  seq[int(site[0]):int(site[1])]
#	if choice_site.count('GG',0,len(choice_site)) >= 1:
#		pattern = re.findall(r'[ACGT]{21}GG',choice_site)
#		print pattern
#	else:
#		print site,'this site has no alternative choice NGG to narrow the gap'

#d = {}
#for site in choice:
#       choice_site =  seq[int(site[0]):int(site[1])]
#       if choice_site.count('GG',0,len(choice_site)) >= 1:
#               pattern = [m.start() for m in re.finditer('GG',choice_site)]
#               d[site[2]] = pattern
#       else:
#               print site,'this site has no alternative choice NGG to narrow the gap'
#print d

def findSite(choice,site):
	d = {}
	for site in choice:
	       choice_site =  seq[int(site[0]):int(site[1])]
	       if choice_site.count('GG',0,len(choice_site)) >= 1:
		       seq_pattern = re.findall(r'[ACGT]{21}GG',choice_site)
	               site_pattern = [m.start() for m in re.finditer('[ATCG]{21}GG',choice_site)]
	               d[site[2]] = (site_pattern,seq_pattern,site[0])
	       else:
	               print site,'this site has no alternative choice NGG to narrow the gap'
	return d


def findSeq(choice,seq):
	seq_patterns = []
	for site in choice:
	       choice_site =  seq[int(site[0]):int(site[1])]
	       if choice_site.count('GG',0,len(choice_site)) >= 1:
	               seq_pattern = re.findall(r'[ACGT]{21}GG',choice_site)
	               seq_patterns.append(seq_pattern)
	       else:
	               print site,'this site has no alternative choice NGG to narrow the gap'
	return seq_patterns
d = findSite(choice,seq)
#print d
gap = 200
now = []
final_result=[]
for k in d.keys():
	for i in range(int(k)//int(gap)):
		minsites = [abs(int(x) - (gap*(i+1)-100)) for x in d[k][0]]
		print >>output, '\t'.join(['chrMT',str(int(d[k][2])+int(d[k][0][minsites.index(min(minsites))])),str(int(d[k][2])+int(d[k][0][minsites.index(min(minsites))])+23),d[k][1][minsites.index(min(minsites))]])
#		print minsites
#		print 'chrMT',str(d[k][2]+int([minsites.index(min(minsites))])),str(d[k][2]+int([minsites.index(min(minsites))])+230,d[k][1][minsites.index(min(minsites))]
#		print now	
#	final_result.append(d[k][minsites.index(min(minsites))])
#	print final_resulti
output.close()
