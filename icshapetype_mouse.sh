#!/bin/bash
echo $1
awk -F'\t|\"|;' 'BEGIN {x=0;}NR==FNR{a[$1]=1;b[$1]=$2}NR>FNR {if($3 == "transcript"&&a[$16]==1){print $28;}}' $1 ~/sunlei/data/mouse/rawdata/Mus_musculus.GRCm38.81.gtf |sort |uniq -c >$1.type.number
python ~/sunlei/sw/myscript/icshapetype.py $1.type.number
rm $1.type.number



