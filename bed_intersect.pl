#! /usr/bin/perl -w
use strict;

die "input file error! $0 gene.bed RBP.bed output.bed 1>partial.RBP 2>no_overlap.RBP" if scalar(@ARGV)!=3;

open GENE,'<',$ARGV[0];

####### read gene bed file
my %gene_location;
while(<GENE>){
	chomp;
	my @line=split;
	$line[0]='chr'.$line[0];
	#### start,end,gene_ID,strand
	push @{$gene_location{$line[0]}},[$line[1],$line[2],$line[3],$line[5]]
	
}

foreach my $chr_ID (keys %gene_location){
	#sort blocks
	@{$gene_location{$chr_ID}}=sort {$a->[0]<=>$b->[0]} @{$gene_location{$chr_ID}};

	##optional:check wether there are overlaps between genes
	# for (my $i =0;$i<scalar(@{$gene_location{$chr_ID}})-2;$i++){
		# if ($gene_location{$chr_ID}->[$i]->[1]>$gene_location{$chr_ID}->[$i+1]->[0]){
			#die "gene overlap found:$chr_ID $i";
		# }
	# }
}


####### process RBP bed file
open RBP,'<',$ARGV[1];
open OUT,'>',$ARGV[2];
while(<RBP>){
	chomp;
	my @line=split;
	my $out_string;
	foreach my $ref_gene (@{$gene_location{$line[0]}}){
	
		# RBP ahead of gene
		next if ($line[2]<=$ref_gene->[0]);
		# RBP behind gene, no need to check following genes
		next if ($line[1]>=$ref_gene->[1]);
		
		if (not($line[1]>=$ref_gene->[0] && $line[2]<=$ref_gene->[1])){
			print "partial overlap between gene and RBP, ignore: $_\n"
		}
		else{
			### finally start position convertion
			$out_string=$line[0]."\t".$line[1]."\t".$line[2]."\t".$line[3]."\t".$line[4]."\t";
			if ($ref_gene->[3] eq $line[5]){
				### gene and RBP: ++/--
				$out_string.='+'."\t".$line[1]."\t".$line[2]."\t".$ref_gene->[2]."\t";
			}
			else{
				### gene and RBP: +-/-+
				$out_string.='-'."\t".$line[1]."\t".$line[2]."\t".$ref_gene->[2]."\t";
			}
			
			###calculate converted position
			if ($ref_gene->[3] eq '+'){
			
			#print "$line[1] $ref_gene->[0] $line[2] $ref_gene->[0]\n";
				$out_string.=($line[1]-$ref_gene->[0])."\t".($line[2]-$ref_gene->[0])."\n";
			}
			else{
				$out_string.=(-$line[2]+$ref_gene->[1])."\t".(-$line[1]+$ref_gene->[1])."\n";
			}
			
			if (defined($out_string)) {print OUT $out_string;}
		}
	}
	if (not defined($out_string)){
		# no overlap with gene found, output to STDERR
		print STDERR $_."\n";
	}
}

close GENE;
close RBP;
close OUT;


