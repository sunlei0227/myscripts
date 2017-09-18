#!/bin/bash
chrom_size=$1
sed '/\_/d' $chrom_size | sed 's/^.../\l/g' >$chrom_size.bw
