#!/bin/bash

#directory /Share/home/zhangqf/sunlei/data/otherdata/RNAmodification/hg38

awk '{print $7}' $1 |sort |uniq |wc -l
#count modificatioin transcript number
awk '$3~/transcript/{print}' ~/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf |wc -l
#count all transcript number
awk '!/^#/{print $4}' $2 |sort|uniq|wc -l
#$2=/Share/home/zhangqf/lipan/DYNAMIC/filter2/invitro/filter100/ch-np/anno_lm.bed  count the vitro dynamic transcript

awk 'NR==FNR{a[$7]=1}NR>FNR{if(a[$4]==1)print $4}' $1 $2|sort|uniq|wc -l
#  count  dynamics' modifaction number


