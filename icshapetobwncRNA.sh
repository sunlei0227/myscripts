#!/bin/bash
icshape_out=$1
#gtf=$2
#fa=$3
#size=$4
#icSHAPE.bedgraph=icSHAPE.bedgraph
#icSHAPE.sorted.bedgraph=icSHAPE.sorted.bedgraph
perl /Share/home/zhangqf/sunlei/sw/icSHAPE/scripts/enrich2BedgraphNcRNA.pl -i $icshape_out -o icSHAPE.bedgraph -g /Share/home/zhangqf/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf  -a /Share/home/zhangqf/sunlei/data/human/Homo_sapiens.GRCh38.ncrna.fa -s /Share/home/zhangqf/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size
sort -k1,1 -k2,3n icSHAPE.bedgraph -o icSHAPE.sorted.bedgraph
perl /Share/home/zhangqf/sunlei/sw/icSHAPE/scripts/uniqueTrack.pl icSHAPE.sorted.bedgraph icSHAPE.sorted.uniq.bedgraph
cut -f1-4 icSHAPE.sorted.uniq.bedgraph | grep -v NULL > icSHAPE.sim.bedgraph
bedGraphToBigWig icSHAPE.sim.bedgraph /Share/home/zhangqf/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size icSHAPE.sim.bw
##for emample perl ~/sunlei/sw/icSHAPE/scripts/enrich2BedgraphGene2.pl -i icshape.out -o icSHAPE.bedgraph -g ~/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf -a ~/sunlei/data/human/Homo_sapiens.GRCh38.dna.primary_assembly_gene_intergene_EN.fa -s ~/sunlei/data/human/primary_assembly_addingXYMT_xk_chr.size 
##gene and transcript is different file


