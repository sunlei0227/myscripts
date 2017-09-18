#!/bin/bash
# $1 is the 
patt=$2
awk '$1~/'$patt'/ {print $0}' $1 |awk '{for(i=6;i<=NF;i++) printf $i""FS;print ""}' |sed -e '/NULL/d' |sort|uniq | awk '{for(i=1;i<=NF;i++){a[i]+=$i};}END{for(i=1;i<NF;i++)printf a[i]/NR"\t" }' >$patt.icshapeprofiling
#sed -e '/NULL/d' $patt.icshape >$patt.noNULL.icshape
#awk '{n=0;for(i=1;i<=NF;i++){a[i]+=$i};print n/NF}END{for(i=1;i<NF;i++)printf a[i]/NR"\t" }' 
