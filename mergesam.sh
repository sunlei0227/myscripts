#!/bin/bash
bowtie2 -p 8 -U $1 -S $1.rRNA.sam -x /Share/home/zhangqf/sunlei/data/human/index/rRNA3index/rRNA  --non-deterministic --time --un $1.unmatched.rRNA
bowtie2 -p 8 -U $1.unmatched.rRNA -S $1.transcript.sam -x /Share/home/zhangqf/sunlei/data/human/index/transcriptomeindex/transcriptome  --non-deterministic --time --un $1.unmatched.transcript
bowtie2 -p 8 -U $1.unmatched.transcript -S $1.gene.sam -x /Share/home/zhangqf/sunlei/data/human/index/onlygene_ENindex/gene_EN  --non-deterministic --time --un $1.unmatched.gene

sam1=$1.transcript.sam
sam2=$1.gene.sam
samtools view -b -S $sam1>$sam1.bam
samtools view -b -S $sam2>$sam2.bam
samtools sort $sam1.bam $sam1.sot
samtools sort $sam2.bam $sam2.sot
samtools merge $sam1.all $sam1.sot.bam $sam2.sot.bam
samtools view -h $sam1.all >$sam1.all.sam
mv $sam1.all.sam ${1%%.*}.sam
