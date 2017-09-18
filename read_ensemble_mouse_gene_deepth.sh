#!/bin/bash

awk '$2!~/4/{print $3}' $1|sort |uniq -c |awk '{print $2"\t"$1}'>${1%.*}.gene.readdeepth
awk -F'\t|\"|;' 'BEGIN {x=0;}NR==FNR{a[$1]=1;b[$1]=$2}NR>FNR {if($3 == "gene"&&a[$10]==1){print $10"\t"$22"\t"b[$10];}}' ${1%.*}.gene.readdeepth ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.81.gtf >${1%.*}.gene.ensemble_deep
read_ensemble_deepth.py ${1%.*}.gene.ensemble_deep

