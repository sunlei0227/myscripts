#! /bin/bash

awk 'NR==FNR{a[$1]=1;b[$1]=$0;}NR>FNR{if(a[$1]==1){print $0"\n"b[$1]}}' $1 $2 >merge.icshape.out

###find the same ID line and show it line by line
