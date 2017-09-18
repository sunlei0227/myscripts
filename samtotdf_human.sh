#!/bin/bash

#trimmed = $1
#bowtie2 -U $1 -S $1.tdfsam -x ~/sunlei/data/human/index/genomindex/genome --non-deterministic --time
samtools view -Sbo $1.bam $1
samtools sort $1.bam -o $1.sort
genomeCoverageBed -bg -ibam $1.sort -g /Share/home/zhangqf/sunlei/data/human/hg38.chrom.sizes > $1.bedgraph
java -Xmx1500m -jar /Share/home/zhangqf/shaodi/app/IGVTools/igvtools.jar toTDF $1.bedgraph $1.tdf hg38
