#!/bin/bash
#generate all site of lincRNA and snRNA, snoRNA micRNA and miscRNA.
awk -F'\t|\"|;' '$3~/gene/{print $1"\t"$4"\t"$5"\t"$10"\t"$22"\t"$7}' Homo_sapiens.GRCh38.83.gtf >alltypeRNA.sites

