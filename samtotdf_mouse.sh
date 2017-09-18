#!/bin/bash

samtools view -Sbo $1.bam $1
samtools sort $1.bam $1.sort
genomeCoverageBed -bg -ibam $1.sort.bam -g /Share/home/zhangqf/sunlei/data/mouse/rawdata/mm10.chrom.sizes > $1.bedgraph
java -Xmx1500m -jar /Share/home/zhangqf/shaodi/app/IGVTools/igvtools.jar toTDF $1.bedgraph $1.tdf mm10
