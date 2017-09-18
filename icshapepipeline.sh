#!/bin/bash

bsub -q ZQF /Share/home/zhangqf/sunlei/sw/icSHAPE/icSHAPE_pipeline_pa.pl -i $1 -t $3 -o $5 -c /Share/home/zhangqf/sunlei/sw/icSHAPE/$6

bsub -q ZQF /Share/home/zhangqf/sunlei/sw/icSHAPE/icSHAPE_pipeline_pa.pl -i $2 -t $4 -o $5 -c /Share/home/zhangqf/sunlei/sw/icSHAPE/$6

