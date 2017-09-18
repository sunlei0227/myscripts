import sys

gtffile = sys.argv[1]
with open(gtffile, 'r') as f:
	flag = 0
	fstart_pos = None
	fstop_pos = None
	start_pos = 0
	stop_pos = 0
	while(True):
		line = f.readline()
		if line:
			if line[0] == '#':
				continue
			data = line.strip().split('\t')		
			if data[2] == 'transcript':
				flag = 1
				fstop_pos = None
				fstart_pos = None
				continue
			if flag == 1:
				if data[2] == 'exon':
					if fstop_pos != None:
						chr = data[0]
						start_pos = int(data[3])
						stop_pos = int(data[4])
						if data[6] == '+':
							if start_pos - fstop_pos < 100 and start_pos - fstop_pos > 0:
								print "chr"+chr, fstop_pos, start_pos,".",".","+"
						else:
							if fstart_pos - stop_pos < 100 and fstart_pos - stop_pos > 0:
								print "chr"+chr, fstart_pos, stop_pos,".",".","-"
						fstop_pos = stop_pos
						fstart_pos = start_pos
					else:
						fstop_pos = int(data[4])
						fstart_pos = int(data[3])
				else:
					fstop_pos = None
					fstart_pos = None
					flag = 0
				
		else:
			break
