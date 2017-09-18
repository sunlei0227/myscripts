#!/bin/bash
#bsub parseAlignment -deletion_masking -primer_length 0 -min_map_qual 30 -file_in 293chD1.sam -ref_seqs ~/sunlei/data/human/index/NCBI45SrRNAindex/45SrRNA.fa -out_folder Shape_D1
bsub parseAlignment -deletion_masking -primer_length 0 -min_map_qual 30 -file_in $1 -ref_seqs ~/sunlei/data/human/index/NCBI45SrRNAindex/45SrRNA.fa -out_folder ${1%.*}
#bsub countMutations -file_in 293chD1_45S.txt -ref_seqs ~/sunlei/data/human/index/NCBI45SrRNAindex/45SrRNA.fa -sample_name 293chD1 -target_name 45S -file_out 293chD1_45S.csv -min_phred 30
cd ${1%.*}
bsub countMutations -file_in ${1%.*}_45S.txt -ref_seqs ~/sunlei/data/human/index/NCBI45SrRNAindex/45SrRNA.fa -sample_name ${1%.*} -target_name 45S -file_out ${1%.*}_45S.csv -min_phred 30
