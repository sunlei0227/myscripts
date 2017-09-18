#!/bin/bash
## $1is the list

SRR=$(cat  $1|awk '{print $1}')

echo $SRR

for srr in $SRR

do

#echo $srr
pre6=${srr:0:6}
id=${srr%%-*}
dir=${srr##*-}

if [ ! -d "$dir" ] ; then
    mkdir $dir
fi

/Share/home/zhangqf/.aspera/connect/bin/ascp -i /Share/home/zhangqf/.aspera/connect/etc/asperaweb_id_dsa.openssh -k 1 -T -l200m anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/SRR/$pre6/$id/$id.sra ./$dir/




done

