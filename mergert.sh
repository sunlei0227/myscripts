#! /bin/bash
awk '(NR%2)' $1>$1.only
awk '(NR%2)' $2>$2.only
awk 'NR==FNR{a[$1]=1;b[$1]=$0;}NR>FNR{if(a[$1]==1){print $0"\n"b[$1]}}' $1.only $2.only |sed -n '3,$'p >$1.$2.merge
rm  $1.only $2.only

###find the same ID line and show it line by line
