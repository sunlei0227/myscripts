#! /bin/bash

awk 'NR==FNR{a[$1]=1;b[$1]=$5;}NR>FNR{if(a[$1]==1){print $5"\t"b[$1]}}' $1 $2 |sed -n '2,$'p >$1.$2.merge

###find the same ID line and show it line by line
