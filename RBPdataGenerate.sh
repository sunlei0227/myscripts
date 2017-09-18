#!bin/bash
sort  -t $'\t' -k1,1 -k2n,2 $1 >$1.sorted
python ~/sunlei/sw/myscript/bedIntersect.py $1.sorted $1.uniq
bsub python ~/sunlei/sw/myscript/genoneCoor2GeneCoor.py ~/sunlei/data/human/human.gene.bed $1.uniq $1.geneCoor
python ~/sunlei/sw/myscript/bedIntersect.py $1.geneCoor $1.geneCoor.uniq
python ~/sunlei/sw/myscript/positiveGenerate.py $1.geneCoor.uniq $1.positive.bed
#cut -f1,2,3 $1.positive.bed |sort|uniq >$1.positive.uniq.bed
## python /Share/home/zhangqf/sunlei/sw/myscript/python/randomSample/randomGenome.py /Share/home/zhangqf/sunlei/data/human/hg38.chrom.chr.sizes 500 genomerandomsite 
# the file genomerandomsite can be used to generate the negetive file with the uniq protein bed file 
#by method like upstair to generate the file genomerandomsite.geneCoor , in /Share/home/zhangqf/sunlei/sw/myscript/python/randomSample/genomerandomsite.geneCoor
# the genomerandomsite.geneCoor have 2.8M number

# in the directory /Share/home/zhangqf/sunlei/sw/myscript/python/randomSample/GenomeNegetiveSample   get the negative sample

python /Share/home/zhangqf/sunlei/sw/myscript/python/randomSample/GenomeNegetiveSample/pickle_pos_neg2.py $1.geneCoor  genomerandomsite.geneCoor $1.positive_choice.bed $1.negative_choice.bed $1.partial_choice.bed

#Then choice positive:negative = 1:5 or 1:10 to put the negative to the file /Share/home/zhangqf/sunlei/data/RBP/human2/forxukui/forxukui_Gene_posneg_bed_randome  [file:negative_new patial_new]

# new file : /Share/home/zhangqf/sunlei/data/RBP/human2/forxukui/forxukui_Gene_posneg_bed_randome_5 nad
#/Share/home/zhangqf/sunlei/data/RBP/human2/forxukui/forxukui_Gene_posneg_bed_randome_10 can be the 1:5 and 1:10 file

#according the positive number choice the negative number
sort -R $1.negative_choice.bed |head -NUMBER >$1.negative.bed
#then run the file in ditectory /Share/home/zhangqf/sunlei/forxujun/forlipan/293/forxukui_gene/rt_bd

bsub ~/sunlei/sw/myscript/xujun/icshape/mouse/transcriptCoor/mapwithNeg_sl2_mod_lipan2_forgene_new.py --bed bedfile_new_uniq_5 --fasta ~/sunlei/data/human/index/onlygene_ENindex/Homo_sapiens.GRCh38.dna.primary_assembly_gene_EN.fa --rt rt_bd_gene_file






