#!/bin/bash

bed=$1
awk '$5>0.95 && length($1)<6{print }' $bed >$bed.filter

sort -k1,1 -k2,3n $bed.filter>$bed.sorted

bedtools genomecov -bg -trackopts 'name="${bed%%.*}" visibility=2 description='' color=255,30,30' -i $bed.sorted -g ~/sunlei/data/human/hg38.chrom.chr.sizes >$bed.bedgraph
