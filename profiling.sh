#!/bin/bash

awk '{print "chr"$1"\t"$2-50"\t"$3+50"\t"$4"\t"$9"\t"$6}' $1 >$1.extend.100
python ~/sunlei/sw/myscript/genoneCoor2GeneCoor.py ~/sunlei/data/human/human.gene.bed $1.extend.100  $1.100.genecoor
python negative_random.py ~/sunlei/data/human/human.gene.ensemble.length $1.100.genecoor $1.100.genecoor.negative
awk '{print $9"\t"$10"\t"$11}' $1.100.genecoor >$1.genecoor1 
awk '{print $9"\t"$10"\t"$11}' $1.100.genecoor.negative >$1.negative1
~/sunlei/sw/myscript/xujun/icshape/mouse/transcriptCoor/mapwithNeg_sl2.py  --bed bedfile --fasta ~/sunlei/data/human/index/onlygene_ENindex/Homo_sapiens.GRCh38.dna.primary_assembly_gene_EN.fa --rt rt_bd_file
/Share/home/zhangqf/sunlei/sw/myscript/xujun/icshape/mouse/transcriptCoor/dataClean.py ${1%.*}.positive.out $1.positive.out.clean
/Share/home/zhangqf/sunlei/sw/myscript/xujun/icshape/mouse/transcriptCoor/dataClean.py ${1%.*}.negative.out $1.negative.out.clean

python meanprofiling.py $1.positive.out.clean 
python meanprofiling.py $1.negative.out.clean 
