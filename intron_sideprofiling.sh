#!/bin/bash

## $1 is the input file which is bed6 and position 6 is the strand information
awk '{if($6 == "+"){print $1"\t"$2-11"\t"$2-1"\t"$4"\t"$5"\t"$NF"\n"$1"\t"$3+1"\t"$3+15"\t"$4"\t"$5"\t"$NF } else {print $1"\t"$3+1"\t"$3+11"\t"$4"\t"$5"\t"$NF"\n"$1"\t"$2-1"\t"$2-15"\t"$4"\t"$5"\t"$NF}}' $1 >$1.position.bed

sed '1,2d' $1.position.bed |sort -k 1,1 >$1.position.bed.sort

python ~/xujun/scripts/icshape/mouse/map.py $1.position.bed.sort seq_str.bed str.out 0

awk 'BEGIN{FS=",";} {print $0,NF}' str.out >1

awk '$6~/11/ {print $0}' 1 >str_fore.bed

awk '$6~/15/ {print $0}' 1 >str_back.bed

awk '{print $5}' str_fore.bed | awk 'BEGIN{FS="," ;OFS="\t";}{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11}' |sed -e '/NULL/d' | awk '{for(i=1;i<=NF;i++){a[i]+=$i};}END{for(i=1;i<NF;i++)printf a[i]/NR"\t" }'>str_fore.profile

awk '{print $5}' str_back.bed | awk 'BEGIN{FS="," ;OFS="\t";}{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15}' |sed -e '/NULL/d' | awk '{for(i=1;i<=NF;i++){a[i]+=$i};}END{for(i=1;i<NF;i++)printf a[i]/NR"\t" }'>str_back.profile

