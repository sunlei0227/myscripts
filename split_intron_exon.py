
import re

gene_bed = '/Share/home/zhangqf/lipan/DYNAMIC/GTF/human_gene.bed'
icSHAPE = '/Share/home/zhangqf/sunlei/figure/icSHAPE_score/HEK293/gene/293_cy_vivo_gene.icshape.out'
OUT_exon = '/Share/home/zhangqf/lipan/split_icshape/human/cy_vivo_exon.txt'
OUT_intro = '/Share/home/zhangqf/lipan/split_icshape/human/cy_vivo_intro.txt'

def gene_type(raw_type):
	"Convert Raw Gene Type to Our Defined Gene Type"
	valid_gene_type = ('protein_coding', 'pseudogene','snRNA','miRNA','misc_RNA','snoRNA','rRNA')
	lncRNA_class = ('3prime_overlapping_ncrna', 'antisense', 'lincRNA', 'processed_transcript', 'sense_overlapping', 'sense_intronic', 'macro_lncRNA')
	if raw_type in valid_gene_type: return raw_type;
	if re.match('.*pseudogene',raw_type) or re.match('disrupted.*',raw_type): return 'pseudogene';
	if raw_type in lncRNA_class: return 'lncRNA';
	return 'other'

def str2arr(mstr):
	myArr = []
	arr = mstr.split(',')
	for a in arr:
		items = a.split('-')
		myArr.append([int(items[0]), int(items[1])])
	return myArr

geneBed = dict()
H = open(gene_bed)
line = H.readline()
while line:
	arr = line.strip().split()
	geneBed[arr[3]] = dict()
	geneBed[arr[3]]['type'] = gene_type(arr[4])
	geneBed[arr[3]]['exon'] = str2arr(arr[5])
	line = H.readline()

def loadicSHAPE(file_name):
	H = open(file_name)
	icBed = dict()
	line = H.readline()
	while line:
		arr = line.strip().split()
		if int(arr[1]) == geneBed[arr[0]]['exon'][-1][1]:
			icBed[arr[0]] = arr[3:]
		else:
			print arr[0]
		line = H.readline()
	return icBed

icBed = loadicSHAPE(icSHAPE)


OUT_INTRO = open(OUT_intro,'w')
OUT_EXON = open(OUT_exon, 'w')

def parseIntro(exon):
	intro = []
	for i in range(len(exon)-1):
		intro.append([exon[i][1]+1, exon[i+1][0]-1])
	return intro

for gene_id in icBed:
	exon_arr = geneBed[gene_id]['exon']
	intro_arr = parseIntro(geneBed[gene_id]['exon'])
	for exon in exon_arr:
		mstr = gene_id + '\t' + geneBed[gene_id]['type'] + '\t' + `exon[0]` + '\t' + `exon[1]` + '\t' + '\t'.join(icBed[gene_id][(exon[0]-1):exon[1]]) + '\n'
		OUT_EXON.writelines(mstr)
	for intro in intro_arr:
		mstr = gene_id + '\t' + geneBed[gene_id]['type'] + '\t' +  `intro[0]` + '\t' + `intro[1]` + '\t' + '\t'.join(icBed[gene_id][(intro[0]-1):intro[1]]) + '\n'
		OUT_INTRO.writelines(mstr)

OUT_INTRO.close()
OUT_EXON.close()







