#!/bin/bash

for i in `ls *bed`;
    do 	sort -n -k 11 $i | tail -2000 > $i.filter;
#    mkdir filter;
    mv $i.filter filter;

done
