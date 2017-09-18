#!/Share/home/zhangqf/usr/anaconda/bin/python
import re
import getopt
import sys

# python mapwithNeg.py ~/xujun/data/CLIP/human/transcriptCoor/RBM10_HITS-CLIP_Piranha_0.001.bed negative.bed ~/xujun/data/FASTA/human/transcriptome.fa positive.out negative.out D1.rt D2.rt D1.bd D2.bd N1.rt N2.rt N1.bd N2.bd ...[other fraction and other vivo and vitro]

#invitro_icshapeFile = sys.argv[1]
#invivo_icshapeFile = sys.argv[2]

Usage = """
Usage: bin.py --bed BedFile --fasta fastaFile --rt rt_bd_File [--filter mean|median] [--cutoff <float>]

--filter	specify whether filter segments according to their RT by mean or median. 
		[Default: no filter]
--cutoff	the cutoff of mean or median. will be ignored if not define --filter
		[Default: 200]

##	==========The Format of BedFile===========
PositiveBedFile1   NegtiveBedFile1   OutPutPositiveFile1   OutPutNegtiveFile1
PositiveBedFile2   NegtiveBedFile2   OutPutPositiveFile2   OutPutNegtiveFile2
............

##	==========The Format of rt_bd_File==========
rt:/Share/home/zhangqf/sunlei/293chD1.only.rt rt:/Share/home/zhangqf/sunlei/293chD2.only.rt 
bd:/Share/home/zhangqf/sunlei/293chD1.only.bd bd:/Share/home/zhangqf/sunlei/293chD2.only.bd
............
[files are splited by \\t or \\n. The output will be in accordance with the order of this file]
"""


opts, args = getopt.getopt(sys.argv[1:],"h",["bed=","fasta=","rt=","filter=","cutoff="])

BedFile = ''; fastaFile = ''; rt_bd_File = ''; cutoff = 200; filter_type = 'None';

for op, value in opts:
	if op == '--bed':
		BedFile = value;
	elif op == '--fasta':
		fastaFile = value;
	elif op == '--rt':	
		rt_bd_File = value;
	elif op == '--filter':
		filter_type = value;
	elif op == '--cutoff':
		cutoff = value;
	elif op == '-h':
		print Usage
		exit(-1)

if filter_type != 'None':
	if filter_type != 'mean' and filter_type != 'median': 
		print 'ERROR: filter_type: ', filter_type
		print Usage
		exit(-1)

if BedFile=='' or fastaFile=='' or rt_bd_File=='': print Usage; exit(-1) 


print 'Start Loading --bed.....'
iPosBeds = []; iNegBeds = []; oPosFile = []; oNegFiles = [];
H = open(BedFile)
line = H.readline()
while line:
	items = line.strip().split()
	if len(items) == 0: line = H.readline(); continue #Empty Line
	if len(items) != 4: print 'Warning: Error Format of BedFile',line; exit(-1);
	iPosBeds.append(items[0]); iNegBeds.append(items[1]); oPosFile.append(items[2]); oNegFiles.append(items[3])
	line = H.readline();


def readBed(bed):
	print "readBed..."
	bedData = []
	with open(bed, 'r') as f:
		lines = f.readlines()
		for line in lines:
			arr = line.strip().split("\t")
			bedData.append([arr[0], arr[1], arr[2], arr[3]])
	return bedData


def readEnsembl(icshape):
	sys.stdout.write("read "+icshape+"......");
	ensemblSet = list(); lenSet = dict();
	count = 0; thousand = 0;
	with open(icshape, 'r') as f:
		line = f.readline()
		while line:
			arr = line.strip().split()
			ensemblSet.append(arr[0]); lenSet[arr[0]] = int(arr[1]) 
			line = f.readline()
			count += 1
			if count==1000: count=0; thousand+=1; sys.stdout.write('.'); sys.stdout.flush();
	sys.stdout.write('\n');
	return ensemblSet, lenSet


def readFasta(fasta):
	print "read " + fasta + "....."
	fasta_seq = {}
	fasta_len = {}
	with open(fasta, 'r') as f:
		line = f.readline()
		ensembl = ""
		seq = ""
		while line:
			if line[0] == '>':
				if ensembl != "":
					fasta_seq[ensembl] = seq
					fasta_len[ensembl] = len(seq)
				ensembl = re.findall("(ENS\w+)",line)[0]
				seq = ""
			else:
				seq += line.strip()	
			line = f.readline()
		fasta_seq[ensembl] = seq
		fasta_len[ensembl] = len(seq)
	return fasta_seq, fasta_len
				
fasta_seq, fasta_len = readFasta(fastaFile)
#fasta_seq, fasta_len = readFasta(fastaFile)

##	====================Load the RTFile List=====================
RTFileList = list()
BDinRTFileList = list()
H = open(rt_bd_File)
line = H.readline()
index  = 0
while line:
	my_list = line.strip().split()
	for item in my_list: 
		result = item.split(':'); 
		if result[0] == 'bd': BDinRTFileList.append(int(index))
		RTFileList.append(result[1])
	line = H.readline()
	index += 1
H.close()

##	====================Start Read File And Intersect=====================
print 'Start Read File And Intersect.......'
intersect = fasta_seq.keys();

def _intersect(g1, g2):
	"g1 and g2 are lists"
	sys.stdout.write('Group1: '+str(len(g1))+"  "+"Group2: "+str(len(g2))+"\n"); sys.stdout.flush();
	intersection = list(); not_found_set = list()
	g2 = sorted(g2); g2_len = len(g2)
	count = 0; thousand = 0;
	for i in range(len(g1)):
		"Bi Search"
		lower = 0; upper = g2_len-1;
		while lower <= upper:
			if g2[(upper+lower)/2] == g1[i]: break;
			elif g2[(upper+lower)/2] < g1[i]: lower = (upper+lower)/2+1;
			else: upper = (upper+lower)/2-1;
		if g2[(upper+lower)/2] == g1[i]: intersection.append( g1[i] )
		else: not_found_set.append( g1[i] )
		count += 1
		if count==1000: count=0; thousand+=1; sys.stdout.write('.'); sys.stdout.flush();
	sys.stdout.write('\n');
	return intersection, not_found_set


lenSet = list()
for file in RTFileList:
	print 'Read File:',file,'.....'
	tmp_ensembl,tmp_lenSet = readEnsembl(file)
	intersect, not_found_set = _intersect( tmp_ensembl, intersect )
	for item in not_found_set: del tmp_lenSet[item]
	lenSet.append(tmp_lenSet) 

print 'After Intersection: ', len(intersect)

##	===========Read icSHAPE Data The Redundant Data==============
intersect.sort();
def _is_intersect(item):
	"item should be a Ensembl ID"
	lower = 0; upper = len(intersect)-1;
	while lower <= upper:
		if intersect[(upper+lower)/2] == item: return (upper+lower)/2+1;
		elif intersect[(upper+lower)/2] < item: lower = (upper+lower)/2+1;
		else: upper = (upper+lower)/2-1;
	return 0;

##	=============Define Mean/Median Function==========
def mean(x):
	return sum([float(i) for i in x])/len(x)

def median(x):
	tmp_x = x[:]; tmp_x = [float(i) for i in tmp_x]; tmp_x.sort()
	if len(x)%2 == 0: return (tmp_x[len(x)/2-1]+tmp_x[len(x)/2])/2
	if len(x)%2 == 1: return tmp_x[len(x)/2]

def filter(array):
	"Array should be an list of floats or strings"
	if filter_type == 'mean':
		if mean(array) >= cutoff: return 1;
		else: return 0;
	if filter_type == 'median':
		if median(array) >= cutoff: return 1;
		else: return 0;	
	print 'Error in filter(array)'
	exit(-1)

RTDataList = list(); index = 0;
for file in RTFileList:
	print 'Read:',file
	RTDataList.append(dict());
	H = open(file)
	line = H.readline()
	count = 0;
	while line:
		count += 1;
		if count==1000: sys.stdout.write('.'); sys.stdout.flush(); count = 0;
		items = line.strip().split()
		if len(items)==0: line = H.readline(); continue
		if _is_intersect(items[0]):
			#Attention Please, the RT has one more site at the first base 
			RTDataList[index][items[0]] = ','.join([str(int(float(i))) for i in items[4:]])
		line = H.readline()
	index += 1
	H.close()
print "After Filter: ",len(intersect)


for i in range( len(oPosFile) ):
	print 'Start output file: ',oPosFile[i], oNegFiles[i]
	positiveOUT = open(oPosFile[i], 'w'); negativeOUT = open(oNegFiles[i],'w'); pBedData = readBed(iPosBeds[i]); nBedData = readBed(iNegBeds[i])
	##	===============Start the First For Loop=================
	count = 0; filter_count = 0;
	for data in pBedData:
		ensembl = data[0]
		start = int(data[1])
		end = int(data[2])
		if not _is_intersect(ensembl):	continue
		same_len = 1
		for i in range(len(lenSet)): 
			if fasta_len[ensembl] != lenSet[i][ensembl]: same_len = 0; break
		if not same_len: continue
		if  end > fasta_len[ensembl]: print 'Warning: The End position in Bed exceed length of',ensembl,'Start:'+str(start)+' End: '+str(end)+' length:'+str(fasta_len[ensembl]); continue;
		mLine = ensembl + "\t" + str(start) + "\t" + str(end) + "\t" + fasta_seq[ensembl][start:end] + "\t";
		if filter_type != 'None':
			flag = 1	
			for k in BDinRTFileList: 
				#Filter will return 0 if numbers are below cutoff
				if filter(RTDataList[k][ensembl].split(',')[start:end]): flag = 0; break;
			if flag == 1: filter_count += 1; continue;
		for k in range(len(RTDataList)): mLine += ','.join(RTDataList[k][ensembl].split(',')[start:end])+"\t";
		positiveOUT.writelines(mLine+data[3]+'\t1\n')
		count += 1
		if count == 100: sys.stdout.write("."); sys.stdout.flush(); count = 0;
	sys.stdout.write("\n"); print 'filter count: ', filter_count;
	##	================Start the Second For Loop====================
	count = 0;filter_count=0;
	for data in nBedData:
		ensembl = data[0]
		start = int(data[1])
		end = int(data[2])
		if not _is_intersect(ensembl):	 continue
                same_len = 1
                for i in range(len(lenSet)):
                        if fasta_len[ensembl] != lenSet[i][ensembl]: same_len = 0; break
                if not same_len: continue
		if  end > fasta_len[ensembl]: print 'Warning: The End position in Bed exceed length of',ensembl,'Start:'+str(start)+' End: '+str(end)+' length:'+str(fasta_len[ensembl]); continue;
                mLine = ensembl + "\t" + str(start) + "\t" + str(end) + "\t" + fasta_seq[ensembl][start:end] + "\t";
                if filter_type != 'None':
                        flag = 1
                        for k in BDinRTFileList:
				#if there exist one BD above 1, we will conserve it
                                if filter(RTDataList[k][ensembl].split(',')[start:end]): flag = 0; break;
                        if flag == 1: filter_count += 1; continue;
                for k in range(len(RTDataList)): mLine += ','.join(RTDataList[k][ensembl].split(',')[start:end])+"\t";
		negativeOUT.writelines(mLine+data[3]+'\t1\n')
		count += 1;
		if count == 100: sys.stdout.write("."); sys.stdout.flush(); count = 0;
	sys.stdout.write("\n"); print 'filter count: ', filter_count;
	positiveOUT.close(); negativeOUT.close();
