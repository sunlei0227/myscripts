#!/bin/bash

CHR='ch'
INVIVO='invivo'
TRANSCRIPT='gene'
OUTPUT='/Share/home/zhangqf/xujun/data/OUTPUT/human/myout'

if [ ! -f $OUTPUT/${INVIVO}_${TRANSCRIPT}_${CHR}.out];
then
if [ $TRANSCRIPT == 'gene' ];
then
	echo 'gene'
	perl geneDataGenerate.pl -i ~/xujun/forxujun/$CHR/$INVIVO/$TRANSCRIPT -a ~/xujun/data/FASTA/human/gene.fa -g ~/xujun/data/GTF/human/Homo_sapiens.GRCh38.83.gtf -o $OUTPUT/${INVIVO}_${TRANSCRIPT}_${CHR}.out
else
	echo 'transcript'
perl dataGenerate.pl  -i ~/xujun/forxujun/$CHR/$INVIVO/$TRANSCRIPT -a ~/xujun/data/FASTA/human/transcriptome.fa -o $OUTPUT/${INVIVO}_${TRANSCRIPT}_${CHR}.out
fi
fi

BEDPATH='/Share/home/zhangqf/xujun/data/OUTPUT/human/CLIP_EXTEND'
OUTPATH="/Share/home/zhangqf/xujun/data/OUTPUT/human/myout/MAPOUT/$CHR/$INVIVO/$TRANSCRIPT"

mkdir -p $OUTPATH

for file in $BEDPATH/*.bed
do
        filename=${file##*/}
        echo $filename
        python map_ensembl.py $file $OUTPUT/${INVIVO}_${TRANSCRIPT}_${CHR}.out $OUTPATH/$filename 0
done


python protein2ensembl.py $OUTPATH $OUTPUT/ensembl.out.${INVIVO}_${TRANSCRIPT}_${CHR}
