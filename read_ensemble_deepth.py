#!/Share/home/zhangqf/usr/anaconda/bin/python
import sys

ensemle = sys.argv[1]
col = 0
d = dict()
with open(ensemle, 'r') as f:
	lines = f.readlines()
      	for line in lines:
 	     	arr = line.strip().split("\t")
		d[arr[1]] = d.get( arr[1], 0 ) + int(arr[2] )
list_pseudogene = []
list_lincRNA = []
others = []
rRNA = []
for k in d:
	if k == "protein_coding":
		print k+"\t"+str(d[k])
	if k == "snoRNA":
		print k+"\t"+str(d[k])
	if k == "snRNA":
		print k+"\t"+str(d[k])
	if k == "miRNA":
		print k+"\t"+str(d[k])
	if k == "misc_RNA":
		print k+"\t"+str(d[k])
	if k in ['rRNA','Mt_rRNA']:
		rRNA.append(d[k])
#		print k+"\t"+str(d[k])
	if k in ['unitary_pseudogene','IG_C_pseudogene','polymorphic_pseudogene','transcribed_unitary_pseudogene','TR_V_pseudogene','unprocessed_pseudogene','IG_V_pseudogene','pseudogene','transcribed_unprocessed_pseudogene','transcribed_processed_pseudogene','processed_pseudogene','transcribed_unitary_pseudogene',]:
		list_pseudogene.append(d[k])
#		print "pseudogene"+'\t'+ sum()
	if k in ['lincRNA','sense_intronic','antisense','processed_transcript','3prime_overlapping_ncrna','macro_lncRNA','sense_intron','bidirectional_promoter_lncrna','sense_overlapping','processed_transcript','antisense']:
		list_lincRNA.append(d[k])
#	else:
#		others.append(d[k])
		
print "pseudogene"+"\t"+str(sum(list_pseudogene))+"\n"+"lncRNA"+"\t"+str(sum(list_lincRNA))+'\n'+'rRNA'+'\t'+ str(sum(rRNA))
		
	
