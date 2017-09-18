#!/bin/bash
awk 'NR%2{j=1;sum=0;for(i=4;i<NF;i++){if($i!="NULL"){sum+=$i;j++;}};print $1"\t"$2"\t"$3"\t"j"\t"sum/j;}' $1 |awk '{sum+=$5}END{print sum/NR}' 
