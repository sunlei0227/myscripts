#!/bin/bash

#this is for the SNV calling
#the reads should map to genome(have the chromsome site)

bowtie2 -p 12 -U $1 -S ${1%%.*}.sam -x ~/sunlei/data/mouse/index/genomindex/genome --non-deterministic --time

#java -jar ~/usr/picard-tools-2.1.1/picard.jar CreateSequenceDictionary R=Mus_musculus.GRCm38.dna.primary_assembly.fa O=Mus_musculus.GRCm38.dna.primary_assembly.dict  ##before using,we should confer it have the .dict

java -jar  ~/usr/picard-tools-2.1.1/picard.jar AddOrReplaceReadGroups I=${1%%.*}.sam O=${1%%.*}.bam SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample

java -jar ~/usr/picard-tools-2.1.1/picard.jar MarkDuplicates I=${1%%.*}.bam O=${1%%.*}.dedupped.bam  CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=output.metrics
#if dont have the dict, we should do it with CreateSequenceDictionary
java -jar  ~/usr/picard-tools-2.1.1/picard.jar CreateSequenceDictionary -r ~/sunlei/data/human/fa/Homo_sapiens.GRCh38.dna.primary_assembly.fa -o ~/sunlei/data/human/fa/Homo_sapiens.GRCh38.dna.primary_assembly.dict

java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T SplitNCigarReads -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -I ${1%%.*}.dedupped.bam -o ${1%%.*}.split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS #splitN calibration

java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T SplitNCigarReads -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -I $1 -o ${1%%.*}.split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS #splitN calibration 

java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T HaplotypeCaller -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -I ${1%%.*}.split.bam -dontUseSoftClippedBases -stand_call_conf 20.0 -stand_emit_conf 20.0 -o ${1%%.*}.vcf #call SNV


java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T VariantFiltration -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -V ${1%%.*}.vcf -window 35 -cluster 3 -o ${1%%.*}.filter.vcf

java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T SelectVariants -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -V ${1%%.*}.filter.vcf -selectType SNP -o ${1%%.*}.filter.snps.vcf  #only exact the snps

java -jar ~/gongjing/software/GenomeAnalysisTK.jar -T SelectVariants -R ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.dna.primary_assembly.fa -V ${1%%.*}.filter.vcf -selectType INDEL -o ${1%%.*}.filter.indels.vcf #only exact the indels

