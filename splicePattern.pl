#! /Share/home/zhangqf/usr/perl-5.22.1/bin/perl 
use warnings;
use strict;
use Getopt::Std;

use lib "/Share/home/zhangqf/sunlei/sw/icSHAPE/module";
use IO qw( &readGTF &readFasta);
use vars qw ($opt_i $opt_o $opt_g $opt_m $opt_n $opt_a);
&getopts('i:o:g:m:n:a:');

=pod
my $usage = <<MESSAGE;
## -----------------------------------
Idenfity icSHPAE value for splicing site
splicePattern.pl -g /Share/home/zhangqf/xujun/data/GTF/human/Homo_sapiens.GRCh38.83.gtf -i icSHAPE.out_filter-length300 -a ~/xujun/data/FASTA/human/gene.fa -m 15 -n 15

Command:
 -i	icSHAPE file
 -g     GTF file
 -a     gene Fasta file
 -m     intron extend
 -n     exon extend

MESSAGE
;
=cut

&main();


sub main
{
	my %parameters = &init();
	my $icSHAPE = readIcshape ( $parameters{icSHAPE} );
	#my (%icSHAPE ) = readIcshape ( $parameters{icSHAPE} );
	#print "\n";
	#for my $mykey (keys %{$icSHAPE}) {
	#	print $mykey,"\t";
	#	if (not $mykey =~ "ENSG" ) {
	#		print keys %{$mykey},"tag\t";
	#	}
	#}
		
	my $ref_annotation = readGTF ( $parameters{gtfFile},
		attribute => "gene_id",
		source => $parameters{gtfSource},
		verbose => 1,
		skip => "Blat" );
	my ($fasta_sequence, $fasta_len, $tmp) = readFasta( $parameters{fastaFile} );
		
	open OUTPUT, "> $parameters{output}" or die "Error in opening output $!\n";
	for my $ensemblID (keys %{$icSHAPE} ) {
		if( not defined $ref_annotation->{$ensemblID} or not defined $fasta_sequence->{$ensemblID} ) {
			print STDERR "Error! $ensemblID not found in gtf file or fasta file!\n";
			next;
		#	print $ensemblID[0];
		}
		#if( not defined $fasta_sequence->{$ensemblID} ) {
		#	print STDERR "Error! $ensemblID not found in gene fasta file!\n";
		#}
		#print  $ref_annotation->{$ensemblID}{gene}{strand};
		#print  $ref_annotation->{$ensemblID}{gene}{strand}[0];
		my @icshapeData;
		my $seqData = ">".$fasta_sequence->{$ensemblID};;
		if ( $ref_annotation->{$ensemblID}{gene}{strand}[0] eq '+' ) {
			 @icshapeData = @{$icSHAPE->{$ensemblID}->{data}}; 
			 #$seqData = $fasta_sequence->{$ensemblID};
		}
		else {
			@icshapeData = reverse(@{$icSHAPE->{$ensemblID}->{data}}); 
			#$seqData = scalar reverse $fasta_sequence->{$ensemblID} ;
		}
		#print @icshapeData;
		#next;
		my $gene_start = $ref_annotation->{$ensemblID}{gene}{start}[0];
		my $gene_len = $ref_annotation->{$ensemblID}{gene}{end}[0] - $gene_start;
		print $gene_len,"\t",$icSHAPE->{$ensemblID}->{len},"\n";
		if( $icSHAPE->{$ensemblID}->{len} != $gene_len ) { print STDERR "Error! $ensemblID len in icSHAPE data not consistent with that in gtf file"; next;}
		for my $exon_index (0..scalar(@{$ref_annotation->{$ensemblID}{exon}{start}})-1) {
			my $exonStart = ${$ref_annotation->{$ensemblID}{exon}{start}}[$exon_index]; 
			my $exonEnd = ${$ref_annotation->{$ensemblID}{exon}{end}}[$exon_index]; 
			print OUTPUT "exon$exon_index\t$ensemblID\t$exonStart\t$exonEnd\t", substr($seqData, $exonStart-$gene_start, $exonEnd-$exonStart),"\t", join("\t", @icshapeData[$exonStart-$gene_start..$exonEnd-$gene_start-1]),"\n";
			if( $ref_annotation->{$ensemblID}{gene}{strand}[0] eq "+" ) {
				if ( $exonStart-$gene_start-$opt_m >= 0) {
					print OUTPUT "exonfiveprime\t$ensemblID\t",$exonStart-$opt_m,"\t",$exonStart+$opt_n-1,"\t", substr($seqData, $exonStart-$gene_start-$opt_m, $opt_n+$opt_m), "\t", join("\t", @icshapeData[$exonStart-$gene_start-$opt_m..$opt_n+$exonStart-$gene_start-1]),"\n";
				}
				if ( $exonEnd+$opt_m-$gene_start < $gene_len) {
					print OUTPUT "exonthreeprime\t$ensemblID\t", $exonEnd-$opt_n, "\t", $exonEnd+$opt_m-1, "\t", substr($seqData, $exonEnd-$gene_start-$opt_n, $opt_m+$opt_n), "\t", join("\t", @icshapeData[$exonEnd-$gene_start-$opt_n..$exonEnd-$gene_start+$opt_m-1]),"\n";
				}
			}
			else {
				if ( $exonStart-$gene_start-$opt_m >= 0) {
                                        print OUTPUT "exonthreeprime\t$ensemblID\t",$exonStart-$opt_m,"\t",$exonStart+$opt_n-1,"\t", substr($seqData, $exonStart-$gene_start-$opt_m, $opt_n+$opt_m), "\t", join("\t", @icshapeData[$exonStart-$gene_start-$opt_m..$opt_n+$exonStart-$gene_start-1]),"\n";
                                }
                                if ( $exonEnd+$opt_m-$gene_start < $gene_len) {
                                        print OUTPUT "exonfiveprime\t$ensemblID\t", $exonEnd-$opt_n, "\t", $exonEnd+$opt_m-1, "\t", substr($seqData, $exonEnd-$gene_start-$opt_n, $opt_m+$opt_n), "\t", join("\t", @icshapeData[$exonEnd-$gene_start-$opt_n..$exonEnd-$gene_start+$opt_m-1]),"\n";
                                }   
			}
		}
		if(defined $ref_annotation->{$ensemblID}{five_prime_utr} ) {
		for my $utr (0..scalar(@{$ref_annotation->{$ensemblID}{five_prime_utr}{start}})-1) {
			my $utrStart = ${$ref_annotation->{$ensemblID}{five_prime_utr}{start}}[$utr];
			my $utrEnd = ${$ref_annotation->{$ensemblID}{five_prime_utr}{end}}[$utr];
			print OUTPUT "five_prime_utr$utr\t$ensemblID\t$utrStart\t$utrEnd\t", substr($seqData,$utrStart-$gene_start,$utrEnd-$utrStart), "\t", join("\t", @icshapeData[$utrStart-$gene_start..$utrEnd-$gene_start-1]),"\n";
		}
		}
		if(defined $ref_annotation->{$ensemblID}{three_prime_utr} ) {
		for my $utr (0..scalar(@{$ref_annotation->{$ensemblID}{three_prime_utr}{start}})-1) {
			my $utrStart = ${$ref_annotation->{$ensemblID}{three_prime_utr}{start}}[$utr];
			my $utrEnd = ${$ref_annotation->{$ensemblID}{three_prime_utr}{end}}[$utr];
			print OUTPUT "three_prime_utr$utr\t$ensemblID\t$utrStart\t$utrEnd\t", substr($seqData, $utrStart-$gene_start, $utrEnd-$utrStart), "\t", join("\t", @icshapeData[$utrStart-$gene_start..$utrEnd-$gene_start-1]),"\n";
		}
		}
			
	}	
		

}




sub init {
	my %parameters = ();

#	die $usage if ( not defined $opt_i || not defined $opt_g );
	
	$parameters{icSHAPE} = $opt_i;
#	$parameters{splice_file} = $opt_s;
	$parameters{gtfFile} = $opt_g;
	$parameters{gtfSource} = "ensembl";
	$parameters{fastaFile} = $opt_a;

	if ( defined $opt_o ) {
		$parameters{output} = $opt_o;
	}
	else { $parameters{output} = "splice_icSHAPE.output"; }
	

	return ( %parameters );
}
	
sub readIcshape
{
        my $icshapeFile = shift;
        my @files = `ls $icshapeFile`;
        my %icshapeData = ();
	my $hash_count = keys %icshapeData;
        my $icshapeID = "";
        my $uniqueCount = 0;
        my $totalCount = 0;
        for my $file (@files)
        {
                open(ICSHAPE, $file) or die "Error in opening icshape file $file\n";
                print STDERR "read icshape file from $file";
                while( my $line = <ICSHAPE> ) {
                        chomp $line;
                        my @data = split(/\t/, $line);
                        $icshapeID = shift @data;
                        $icshapeID =~ s/\.[0-9]*//;
                        $totalCount += 1;
			#print "$icshapeID\n";
                        next if (defined $icshapeData{$icshapeID});
                        $uniqueCount += 1;
                        $icshapeData{$icshapeID}{len} = shift @data;
                        $icshapeData{$icshapeID}{rpkm} = shift @data;
                        $icshapeData{$icshapeID}{data} = \@data;

                }
                close ICSHAPE;

                print "$file uniqueCount=$uniqueCount\ttotalCount=$totalCount\n";
                $uniqueCount = 0;
                $totalCount = 0;
        }

        return ( \%icshapeData );
}

