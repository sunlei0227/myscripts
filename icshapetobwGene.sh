#!/bin/bash
#$icshape_out=$1
#gtf=$2
#fa=$3
#size=$4
#icSHAPE.bedgraph=icSHAPE.bedgraph
#icSHAPE.sorted.bedgraph=icSHAPE.sorted.bedgraph
perl /Share/home/zhangqf/sunlei/sw/icSHAPE/scripts/enrich2BedgraphGene.pl -i $1 -o $1.icSHAPE.bedgraph -g /Share/home/zhangqf/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf -a /Share/home/zhangqf/sunlei/data/human/index/onlygene_ENindex/Homo_sapiens.GRCh38.dna.primary_assembly_gene_EN.fa  -s /Share/home/zhangqf/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size
sort -k1,1 -k2,3n $1.icSHAPE.bedgraph -o $1.icSHAPE.sorted.bedgraph
perl /Share/home/zhangqf/sunlei/sw/icSHAPE/scripts/uniqueTrack.pl $1.icSHAPE.sorted.bedgraph $1.icSHAPE.sorted.uniq.bedgraph
cut -f1-4 $1.icSHAPE.sorted.uniq.bedgraph | grep -v NULL > $1.icSHAPE.sim.bedgraph
bedGraphToBigWig $1.icSHAPE.sim.bedgraph /Share/home/zhangqf/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size $1.icSHAPE.sim.bw
##for emample perl ~/sunlei/sw/icSHAPE/scripts/enrich2BedgraphGene2.pl -i icshape.out -o icSHAPE.bedgraph -g ~/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf -a ~/sunlei/data/human/Homo_sapiens.GRCh38.dna.primary_assembly_gene_intergene_EN.fa -s ~/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size 
##gene and transcript is different file


