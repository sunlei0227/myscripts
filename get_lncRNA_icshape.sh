#!/bin/bash

#打印出所有的转录本的类型：
#awk -F'\t|\"|;' '$3~/transcript/ {print $28}' Homo_sapiens.GRCh38.83.gtf |sort |uniq
#打印出转录本号：
#awk -F'\t|\"|;' '$3~/transcript/ {print $16}' Homo_sapiens.GRCh38.83.gtf

#求icshape 与gtf文件的转录交集：
awk -F . '{print $1}' $1 >$1_nodot
awk -F'\t|\"|;' 'BEGIN {x=0;}NR==FNR{a[$1]=1;}NR>FNR {if($3=="transcript"&&a[$16]==1){print $16"\t"$28;}}' $1_nodot ~/sunlei/data/human/Homo_sapiens.GRCh38.83.gtf  >transcript_type

#重定向之后统计各个种类的个数：
cut -f 2 transcript_type | sort | uniq -c

#grep 'protein_coding' transcript_type > protein_coding_ensemble

#awk 'NR==FNR{a[$1]=1} NR>FNR {if (a[$1]==1) print $0}' protein_coding_ensemble $1_nodot >protein_coding_icshape

awk '{ORS=",";for(i=1;i<=NF;i++) if (i>3&&$i!="NULL") print $i;print "\n"}' $1 | sed 's/^,//g;s/,$//g' |sed '/^$/d' >lncRNA_for_Gini
