import re

H = open('transcriptome.fa')
headers = list()
reObj1 = re.compile('^>(\w+)\s+.*segs:(\S+)')
line = H.readline()
while line:
	if line.startswith('>'):
		results = reObj1.findall(line.strip())
		s_e = results[0][1].split(',')[-1].split('-')
		print results[0][0], s_e[1]
	line = H.readline()

