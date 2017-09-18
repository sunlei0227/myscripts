#!/bin/bash

awk '{ if($2!=4) {print $0} }' $1 > $1.filter.sam

samtools view -Sb $1.filter.sam > $1.bam

bamToBed -i $1.bam > $1.bed

bedtools intersect -wa -a ~/sunlei/data/human/Homo_sapiens.GRCh38.83.bed -b $1.bed >$1.read_ditribution.bed 


