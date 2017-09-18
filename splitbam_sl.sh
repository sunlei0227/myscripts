#! /bin/bash

mkdir ${1%.*}_split
cd ${1%.*}_split
#range = {1..22,X,Y}
for i in `seq 22`;
#for(i=1; i<=22; i++);
do samtools view -b ../$1 $i > ${1%.*}_chr$i.bam;
done

for i in `echo X`;
do samtools view -b ../$1 $i > ${1%.*}_chr$i.bam;
done

for i in `echo Y`;
do samtools view -b ../$1 $i > ${1%.*}_chr$i.bam;
done
