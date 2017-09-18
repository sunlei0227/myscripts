#!/bin/bash

awk '$2!~/4/{print $3}' $1|sort |uniq -c |awk '{print $2"\t"$1}'>${1%.*}.readdeepth
awk -F'\t|\"|;' 'BEGIN {x=0;}NR==FNR{a[$1]=1;b[$1]=$2}NR>FNR {if($3 == "transcript"&&a[$16]==1){print $16"\t"$28"\t"b[$16];}}' ${1%.*}.readdeepth ~/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf >${1%.*}.ensemble_deep
read_ensemble_deepth.py ${1%.*}.ensemble_deep

