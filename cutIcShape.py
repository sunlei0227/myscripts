import re, sys, os, getopt, time


"""
Attention: params['tFile'] should be formated like this:
GENE_ID1 value1
GENE_ID2 value2
.....

"""


treatFile = '/Share/home/zhangqf/sunlei/experiment/dynamic/RNA_processing/translation/ch.translation_efficiency.sorted.simplified'
bedFile = '/Share/home/zhangqf/lipan/DYNAMIC/GTF/Homo_sapiens.trans.bed'
icFile = '/Share/home/zhangqf/sunlei/forlipan/icSHAPE/293/vivo/293ch_transcript_icshape.out'



params = dict()
params['refbed'] = bedFile
params['tFile'] = treatFile
params['icFile'] = icFile

params['UTR5'] = 'utr5.txt'
params['UTR3'] = 'utr3.txt'
params['CDS_HEAD'] = 'cds_head.txt'
params['CDS_TAIL'] = 'cds_tail.txt'
params['LEFT'] = 'LEFT.txt'

params['CDS_HEAD_LEN'] = 100
params['CDS_TAIL_LEN'] = 100

def gene_type(raw_type):
		"Convert Raw Gene Type to Our Defined Gene Type"
		valid_gene_type = ('protein_coding', 'pseudogene', 'snoRNA', 'snRNA', 'miRNA', 'misc_RNA', 'rRNA')
		lncRNA_class = ('antisense','lincRNA','processed_transcript','sense_intronic','TEC','sense_overlapping')
		if raw_type in valid_gene_type: return raw_type;
		if re.match('.*pseudogene',raw_type): return 'pseudogene';
		if raw_type in lncRNA_class: return 'lncRNA';
		return 'other'

##      sort a numbers string and return sorted list
def norm_exons(string):
	tuples = list(); raw_tuple = list()
	arr = string.split(',')
	for indx in range(len(arr)):
		aarr = arr[indx].split('-')
		if indx == 0:  tuples.append( (1, abs(int(aarr[1])-int(aarr[0]))+1 ) )
		else: tuples.append( (tuples[-1][1]+1, abs(int(aarr[1])-int(aarr[0]))+tuples[-1][1]+1 ) )
		raw_tuple.append( (int(aarr[0]), int(aarr[1])) )
	return tuples, raw_tuple

def norm_utr(exon_str, utr_str, strand):
	"strand is neccessery"
	norm_tuple, raw_tuple = norm_exons(exon_str)
	utr_tuple = list() 
	arr = utr_str.split(',')
	for indx in range(len(arr)):
		aarr = [ int(i) for i in arr[indx].split('-') ]
		flag = False
		for i in range(len(raw_tuple)):
			if strand == '-': 
				if raw_tuple[i][0] == aarr[0] < aarr[1] == raw_tuple[i][1]:
					utr_tuple.append( ( norm_tuple[i][0], norm_tuple[i][1] ) ); flag = True; break
				elif raw_tuple[i][0] == aarr[0] <= aarr[1] < raw_tuple[i][1]:
					utr_tuple.append( ( raw_tuple[i][1]-aarr[1]+norm_tuple[i][0], norm_tuple[i][1] ) ); flag = True; break
				elif raw_tuple[i][0] < aarr[0] <= aarr[1] == raw_tuple[i][1]:
					utr_tuple.append( ( norm_tuple[i][0], raw_tuple[i][1]-aarr[0]+norm_tuple[i][0] ) ); flag = True; break
			if strand == '+':
				if raw_tuple[i][0] == aarr[0] < aarr[1] == raw_tuple[i][1]:
					utr_tuple.append( ( norm_tuple[i][0], norm_tuple[i][1] ) ); flag = True; break 
				elif raw_tuple[i][0] == aarr[0] <= aarr[1] < raw_tuple[i][1]:
					utr_tuple.append( ( norm_tuple[i][0], norm_tuple[i][0]+aarr[1]-aarr[0] ) ); flag = True; break
				elif raw_tuple[i][0] < aarr[0] <= aarr[1] == raw_tuple[i][1]:
					utr_tuple.append( ( norm_tuple[i][1]-(aarr[1]-aarr[0]), norm_tuple[i][1] ) ); flag = True; break
		if not flag: print 'Unexpected Result'
	return norm_tuple, utr_tuple

def parseUTR(utr, trans_len):
	"Discriminate 3' or 5' UTR"
	utr_3 = 0; utr_5 = 0;
	if utr[0][0] == 1 and utr[-1][1] != trans_len: #only 5' UTR
		utr_5 = (1, utr[-1][1])
	if utr[0][0] != 1 and utr[-1][1] == trans_len: #only 3' UTR
		utr_3 = (utr[0][0], trans_len)
	if utr[0][0] != 1 and utr[-1][1] != trans_len: #no UTR
		print utr; print trans_len
		print 'NO POSSIBLE'
	if utr[0][0] == 1 and utr[-1][1] == trans_len: # 3' UTR and 5' UTR
		for i in range(len(utr)-1):
			if utr[i][1] != utr[i+1][0] - 1:
				utr_5 = (1, utr[i][1]); utr_3 = (utr[i+1][0], trans_len)
				break
	return utr_5, utr_3


def getFirstExon(trans_name):
	if len(trans[trans_name]['exon']) != 0:
		return trans[trans_name]['exon'][0]
	else:
		return 0

def getLastExon(trans_name):
	if len(trans[trans_name]['exon']) != 0:
		return trans[trans_name]['exon'][-1]
	else:
		return 0

def get_5p_UTR(trans_name):
	if trans[trans_name]['utr_5']:
		return trans[trans_name]['utr_5']
	else:
		return 0;

def get_3p_UTR(trans_name):
	if trans[trans_name]['utr_3']:
		return trans[trans_name]['utr_3']
	else:
		return 0

def getCDSHead(trans_name, max_len):
	if trans[trans_name]['CDS']:
		CDS_tuple = trans[trans_name]['CDS']
		if CDS_tuple[1] - CDS_tuple[0] < max_len:
			return CDS_tuple
		else:
			return (CDS_tuple[0], CDS_tuple[0]+max_len)
	return 0

def getCDSTail(trans_name, max_len):
	if trans[trans_name]['CDS']:
		CDS_tuple = trans[trans_name]['CDS']
		if CDS_tuple[1] - CDS_tuple[0] < max_len:
			return CDS_tuple
		else:
			return (CDS_tuple[1]-max_len, CDS_tuple[1])
	return 0

def getLeftRegion(trans_name, head_len=100, tail_len=100):
	utr_5 = get_5p_UTR(trans_name)
	utr_3 = get_3p_UTR(trans_name)
	cds_head = getCDSHead(trans_name,head_len)
	cds_tail = getCDSTail(trans_name,tail_len)
	lBound = 0; uBound = 99999999;
	if utr_5:
		lBound = utr_5[1]
	if cds_head and lBound < cds_head[1]:
		lBound = cds_head[1]
	if utr_3:
		uBound = utr_3[0]
	if cds_tail and uBound > cds_tail[0]:
		uBound = cds_tail[0]
	if uBound > lBound:
		return (lBound, uBound)
	else:
		return 0






##      ============Load The Ref Bed File=============  ##
INPUT = open(params['refbed'])
line = INPUT.readline()
trans = dict(); trans_name_3 = list(); trans_name_5 = list(); trans_CDS = list(); gene_trans = dict()
while line:
		if line.startswith('#'): line = INPUT.readline(); continue
		arr = line.strip().split()
		utr = tuple(); exon = tuple(); utr_5 = 0; utr_3 = 0
		if len(arr) == 9: #with UTR
			exon, utr = norm_utr(arr[7], arr[8], arr[3])
			if utr: 
				length = sum( [ item[1]-item[0]+1 for item in exon ] )
				utr_5, utr_3 = parseUTR(utr, length)
				if utr_5: trans_name_5.append( arr[5] )
				if utr_3: trans_name_3.append( arr[5] )
		else:   
			try:
				exon = norm_exons( arr[7] )[0]
			except IndexError:
				print arr
				break
		if arr[6] == 'protein_coding': trans_CDS.append( arr[5] )
		length = sum( [ item[1]-item[0]+1 for item in exon ] )
		CDS = [1, length]
		if utr_5: CDS[0] = utr_5[1]+1
		if utr_3: CDS[1] = utr_3[0]-1
		if arr[4] in gene_trans: gene_trans[ arr[4] ].append( arr[5] )
		else: gene_trans[ arr[4] ] = [ arr[5], ] 
		trans[ arr[5] ] = { 'gene':arr[4], 'type':gene_type(arr[6]), 'exon':exon, 'utr':utr, 'length':length, 'utr_5':utr_5, 'utr_3':utr_3, 'CDS':CDS }
		line = INPUT.readline()

INPUT.close()

trans_name_3.sort(); trans_name_5.sort(); trans_CDS.sort();

##	====Load numeric values======
INPUT = open(params['tFile'])
number_Set = dict()
line = INPUT.readline()
while line:  
	arr = line.split()
	number_Set[arr[0]] = arr[1]
	line = INPUT.readline()

INPUT.close()

##	====Load icSHAPE File=====
INPUT = open(params['icFile'])
icshape_Set = dict()
line = INPUT.readline()
while line:  
	arr = line.split()
	icshape_Set[arr[0]] = arr[3:]
	line = INPUT.readline()

INPUT.close()



##	Start to cut icSHAPE
head_len = params['CDS_HEAD_LEN']
tail_len = params['CDS_TAIL_LEN']
UTR5 = open(params['UTR5'],'w')
UTR3 = open(params['UTR3'],'w')
CDS_S = open(params['CDS_HEAD'],'w')
CDS_E = open(params['CDS_TAIL'],'w')
LEFT = open(params['LEFT'],'w')

genes_not_found = list();
for gene in number_Set:
	if gene not in gene_trans:
		genes_not_found.append(gene)
	else:
		all_trans = gene_trans[gene]
		trans_name = all_trans[0]; trans_len = trans[trans_name]['length']
		for i in range(1, len(all_trans)):
			if trans[all_trans[i]]['length'] > trans_len:
				trans_len = trans[all_trans[i]]['length']; trans_name = all_trans[i]
		if trans_name not in icshape_Set:
			print trans_name + ' not in icshape_Set'
			continue
		if len(icshape_Set[trans_name]) != trans[trans_name]['length']:
			print trans_name+' '+gene+' are not the same length'
			continue
		utr_5 = get_5p_UTR(trans_name)
		utr_3 = get_3p_UTR(trans_name)
		cds_head = getCDSHead(trans_name, head_len)
		cds_tail = getCDSHead(trans_name, tail_len)
		left = getLeftRegion(trans_name, head_len, tail_len)
		const_str = trans_name+'\t'+gene+'\t'+number_Set[gene]+'\t'
		if utr_5:
			UTR5.writelines(const_str+str(utr_5[0])+'\t'+str(utr_5[1])+'\t'+'\t'.join(icshape_Set[trans_name][utr_5[0]:utr_5[1]]) + '\n')
		if utr_3:
			UTR3.writelines(const_str+str(utr_3[0])+'\t'+str(utr_3[1])+'\t'+'\t'.join(icshape_Set[trans_name][utr_3[0]:utr_3[1]]) + '\n')
		if cds_head:
			CDS_S.writelines(const_str+str(cds_head[0])+'\t'+str(cds_head[1])+'\t'+'\t'.join(icshape_Set[trans_name][cds_head[0]:cds_head[1]]) + '\n')
		if cds_tail:
			CDS_E.writelines(const_str+str(cds_tail[0])+'\t'+str(cds_tail[1])+'\t'+'\t'.join(icshape_Set[trans_name][cds_tail[0]:cds_tail[1]]) + '\n')
		if left:
			LEFT.writelines(const_str+str(left[0])+'\t'+str(left[1])+'\t'+'\t'.join(icshape_Set[trans_name][left[0]:left[1]]) + '\n')

UTR5.close() 
UTR3.close()
CDS_S.close()    
CDS_E.close()
LEFT.close()

