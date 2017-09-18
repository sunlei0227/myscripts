#!/bin/bash


#for i in `ls *bed`; do awk '{print $1"\t"$2"\t"$3"\t"$5"\t"$11"\t"$6}' $i>$i.bed6; done

#for i in `ls *hg38.bed`;
 #   do bedtools getfasta -fi ~/sunlei/data/human/Homo_sapiens.GRCh38.dna.primary_assembly_addingchr.fa -bed $i -fo ${i#.}.fa ;
#    done
for i in `ls *fa`;
	   do echo $i;
	   fimo --oc $i.fimo ${i%%_*}  $i;
           if [ $? !=0 ]; then continue;fi	
           cd $i.fimo;
#	if [ $? == 0 ]; then
	   awk '{print $1}' fimo.txt >1;
	   awk '{print $3"\t"$4"\t"$5}' fimo.txt >2;
	   awk '{print $2}' fimo.txt >3;
	   awk -F '[:\t-]' '{print $1"\t"$2"\t"$3}' 3 > 4;
	   paste 4 2 > tmp_result
	   awk  '{print $1"\t"$2+$4-1"\t"$2+$5-1"\t"$4"\t"$5"\t"$6}' tmp_result >5;
#	   awk '{print $5}' fimo.txt >2;
           paste 1 5 >the_result;
#	   sort -k 1,1 the_result>
	   awk '!/^#/''{print $0>>$1"'$i'"".sunlei"}' the_result;
           for t in `ls *sunlei`;
	       do awk 'BEGIN {OFS = "\t";}{print $2,$3,$4,$5,$6,$7}' $t|sort -k 1,1  >$t.sort ; mv $t.sort ../;

#	   cd ../;
#fi
done
           cd ../;

done  
