#! /bin/bash

~/sunlei/sw/icSHAPE/scripts/readCollapse.pl -U $1 -o ${1%.*}.rmdp.fastq -f ${1%.*}.fa
~/sunlei/sw/icSHAPE/scripts/trimming.pl -U ${1%.*}.rmdp.fastq -o ${1%.*}.trimmed.fastq -l 13 -t 0 -c phred33 -a ~/sunlei/sw/adaptor -m 25
~/sunlei/sw/myscript/mergesam.sh ${1%.*}.trimmed.fastq

