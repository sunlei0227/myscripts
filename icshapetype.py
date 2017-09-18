import sys
import re

def gene_type(raw_type):
    "Convert Raw Gene Type to Our Defined Gene Type"
    valid_gene_type = ('protein_coding', 'pseudogene','snRNA','miRNA','misc_RNA','snoRNA','rRNA')
    lncRNA_class = ('3prime_overlapping_ncrna', 'antisense', 'lincRNA', 'processed_transcript', 'sense_overlapping', 'sense_intronic', 'macro_lncRNA')
    if raw_type in valid_gene_type: return raw_type;
    if re.match('.*pseudogene',raw_type) or re.match('disrupted.*',raw_type): return 'pseudogene';
    if raw_type in lncRNA_class: return 'lncRNA';
    return 'other'  

list =[]
d ={}
lincRNA =0
pseudogene = 0
other = 0
with open(sys.argv[1],'r') as f:
	line = f.readline()
	while line:
		arr = line.strip().split()
		if arr[1] in ('3prime_overlapping_ncrna', 'antisense', 'lincRNA', 'processed_transcript', 'sense_overlapping', 'sense_intronic', 'macro_lncRNA'):
			lincRNA += int(arr[0])
		if re.match('.*pseudogene',arr[1]) or re.match('disrupted.*',arr[1]) or arr[1]=="pseudogene":
			pseudogene += int(arr[0])
		if arr[1] in ('protein_coding','snRNA','miRNA','misc_RNA','snoRNA','rRNA'):
			print arr[1],arr[0]
		else:
			other += int(arr[0])
#		d[arr[1]] = arr[0]
		line =f.readline()
	print "lincRNA\t",lincRNA,"\n", "pseudogene", pseudogene
	

