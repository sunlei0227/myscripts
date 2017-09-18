#!/usr/bin/perl
use strict;
use warnings;

use lib "$ENV{ICSHAPE}/module";
use Getopt::Std;
use icSHAPEutil qw( &readGTF_ensembl_new );
use Data::Dumper;

use vars qw ($opt_h $opt_V $opt_D $opt_i $opt_o $opt_a $opt_f $opt_s $opt_b $opt_p );
&getopts('hVDi:a:o:f:s:b:p');

my $usage = <<_EOH_;
## --------------------------------------
convert genomic coordinates to transcript coordinates

Command:
$0 -i genome_coordinates -o transcript_coordinates -a annotation_file

# what it is:
 -i     genomic coordinates
 -o     transcript coordinates
 -a     annotation file (GTF format)

# more options
 -f     genomic coordinates format
            bed: normal bed6 format
            simple: no strand information, then both strand will be searched
            single: only one position 
 -s     annotation source. e.g., ensembl (default), gencode, ...
 -b     bin width (if not specified, will be determined from input genomic coordinates)
 -p     print nonoverlapped regions

_EOH_
;

&main ();

sub main {
    my %parameters = &init();

    my $genomeFile = $parameters{genomeFile};
    my $transcriptFile = $parameters{transcriptFile};
    my $annotationFile = $parameters{annotationFile};

    my $ref_position = readGenomePosition ( $genomeFile, format => $parameters{format} );
    my $ref_annotation = readGTF_ensembl_new ( $parameters{annotationFile}, verbose => $opt_V );
    my $ref_bin = binize ( $ref_annotation->{gene_info}, $ref_annotation->{chr_size}, bw => $parameters{bw} );

    &convert ( $ref_position, $ref_annotation, $ref_bin, bw => $parameters{bw} );
    &printPosition ( $ref_position, $transcriptFile, printNonOverlap => $parameters{printNonOverlap} );

    1;
}


## ------------------------------------
sub init
{
    my %parameters = ();
    die $usage if ( $opt_h || ( not $opt_i ) || ( not $opt_o ) || ( not $opt_a ) );

    $opt_V = 0 if ( not defined $opt_V );
    $opt_D = 0 if ( not defined $opt_D );
    my $pwd = `pwd`;  chomp $pwd;

    $parameters{genomeFile} = $opt_i;
    $parameters{transcriptFile} = $opt_o;
    $parameters{annotationFile} = $opt_a;

    if ( defined $opt_f ) { $parameters{format} = $opt_f; }
    else { $parameters{format} = "bed"; }
    if ( defined $opt_s ) { $parameters{annotationSource} = $opt_s; }
    else { $parameters{annotationSource} = "ensembl"; }
    if ( defined $opt_b ) { $parameters{bw} = $opt_b; }
    else { $parameters{bw} = 100000; }
    if ( defined $opt_p ) { $parameters{printNonOverlap} = 1; }
    else { $parameters{printNonOverlap} = 0; }

    return ( %parameters );
}

sub readGenomePosition
{
    my $input_file = shift;
    my %parameters = @_;

    open (IN, "<$input_file") or die ( "Cannot open $input_file for reading!\n" );
    print STDERR "Read positions from file $input_file.\n\t", `date`;
    my @absPosition = ();
    my $count = 0;
    while (my $line = <IN> )  {
        next if ( $line =~ /^#/ );

        chomp $line;
        $absPosition[$count]{info} = $line;
        my ( $chr, $start, $end, $protein, $confidence, $strand ) = split ( /\t/, $line );
        $chr =~ s/^chr//;

        my $format = ( defined $parameters{format} ) ? "$parameters{format}" : "bed";
        if ( $format eq "bed" ) { 
            $absPosition[$count]{chr} = $chr; $absPosition[$count]{strand} = $strand; $absPosition[$count]{confidence} = $confidence;
            $absPosition[$count]{start} = $start; $absPosition[$count]{end} = $end; 
        }
        elsif ( $format eq "simple" ) {
            $absPosition[$count]{chr} = $chr; $absPosition[$count]{strand} = "+";
            $absPosition[$count]{start} = $start; $absPosition[$count]{end} = $end;
            $count++;
            $absPosition[$count]{info} = $line;
            $absPosition[$count]{chr} = $chr; $absPosition[$count]{strand} = "-";
            $absPosition[$count]{start} = $start; $absPosition[$count]{end} = $end;
        }
        elsif ( $format eq "single" ) {
            $absPosition[$count]{chr} = $chr; $absPosition[$count]{strand} = "+";
            $absPosition[$count]{start} = $start; $absPosition[$count]{end} = $start+1;
            $count++;
            $absPosition[$count]{info} = $line;
            $absPosition[$count]{chr} = $chr; $absPosition[$count]{strand} = "-";
            $absPosition[$count]{start} = $start; $absPosition[$count]{end} = $start+1;
        }
        $count++;
    }
    close IN;
    print STDERR "$count positions in total.\n\t", `date`;

    return \@absPosition;
}

sub binize
{
    my $ref_featurePos = shift;
    my $ref_chr_size = shift;
    my %parameters = @_;

    print STDERR "Binize genome to speed up searching.\n\t", `date`;
    my $bw = $parameters{bw};
    my %bin = ();
    foreach my $chr ( keys %{$ref_chr_size} ) {
        my $count = int ( $ref_chr_size->{$chr} / $bw ) + 1;
        for ( my $idx = 0; $idx < $count; $idx++ ) { $bin{$chr}{"+"}[$idx] = ();  $bin{$chr}{"-"}[$idx] = ();  }
    }
    #print "$bw\n";
    foreach my $featureID ( keys %{$ref_featurePos} ) {
        print "$featureID\n";
	my $chr = $ref_featurePos->{$featureID}{chr};
        my $strand = $ref_featurePos->{$featureID}{strand};
        my $start = int ( $ref_featurePos->{$featureID}{start} / $bw );
        my $end = int ( $ref_featurePos->{$featureID}{end} / $bw );
 	#print "$chr\n$strand\n$start\n$end\n";
        for ( my $idx = $start; $idx <= $end; $idx++ ) { print "$chr\t$strand\t$idx\t$featureID\n";push @{$bin{$chr}{$strand}[$idx]}, $featureID; }
	#foreach my $gene ( @{$bin->{$chr}{$strand}[$start]} ) {print "$gene\n";}
    }

    
    return \%bin;
}

sub convert
{
    my $ref_positions = shift;
    my $ref_annotation = shift;
    my $ref_bin = shift;
    my %parameters = @_;


    print STDERR "Checking overlapped transcripts in input positions...\n\t", `date`;
    my $bw = $parameters{bw};
    my $overlapCount = 0;
    for ( my $idx = 0; $idx < scalar ( @{$ref_positions} ); $idx++ ) {
        print STDERR "position $idx\t", `date` if ( $idx and ( $idx % 10000 == 0 ) ); 

        my @overlapRegion = ();
        my $chr = $ref_positions->[$idx]{chr};
        my $strand = $ref_positions->[$idx]{strand};
        my $start = $ref_positions->[$idx]{start};
        my $end = $ref_positions->[$idx]{end};
	#print "$ref_bin->{$chr}{$strand}[$start/$bw][0]\n";
	#print "$chr\t$strand\t$start\t$end\n";
        for ( my $idxBin = int ( $start / $bw ); $idxBin <= int ( $end / $bw ); $idxBin++ ) {
            ## get genes in the bin
        #$chr = "chr".$chr;    
	print "$chr\t$idxBin\n";
            foreach my $gene ( @{$ref_bin->{$chr}{$strand}[$idxBin]} ) {
                # get transcripts for each gene
                print "$gene\n";
                next if ( ( $end < $ref_annotation->{gene_info}{$gene}{start} ) or ( $start > $ref_annotation->{gene_info}{$gene}{end} ) );
                foreach my $transID ( @{$ref_annotation->{gene_info}{$gene}{transcript}} ) {
		print "$transID\n";
                    next if ( ( $end < $ref_annotation->{transcript_info}{$transID}{start} ) or ( $start > $ref_annotation->{transcript_info}{$transID}{end} ) );
                    $overlapCount += &overlapTrans ( \@overlapRegion, $ref_annotation, $transID, $strand, $start, $end );
                    $ref_positions->[$idx]{overlap} = \@overlapRegion;
                }
            }
        }
    }

    return $overlapCount;
}

sub overlapTrans
{
    my $ref_overlapRegion = shift;
    my $ref_annotation = shift; my $transID = shift;
    my $strand = shift; my $absStart = shift; my $absEnd = shift; 

    my $transcript = $ref_annotation->{transcript_info}{$transID};
    my $numExon = scalar ( keys %{$transcript->{exon}} );

    my $overlapCount = 0;
    my $relExonStart = 0;  my $startPosiInExon = 0; my $endPosiInExon = 0; my $absStartInExon = 0; my $absEndInExon = 0; 
    for ( my $idxExon = 1; $idxExon <= $numExon; $idxExon++ ) {
        my $idxExonWithStrand = ( $strand eq "+" ) ? $idxExon : ( $numExon - $idxExon + 1 );
        my $exonID = $ref_annotation->{transcript_info}{$transID}{exon}{$idxExon};
        my $exonStart = $ref_annotation->{exon_info}{$exonID}{start};
        my $exonEnd = $ref_annotation->{exon_info}{$exonID}{end};
        my $exonLength = $exonEnd - $exonStart + 1;
	print "exon:$exonID\t$exonStart\t$exonEnd\n";
        if ( ( $exonStart <= $absEnd ) && ( $exonEnd >= $absStart ) ) {
            ## overlapped
            if ( $strand eq "+" ) {
                $startPosiInExon = $absStart - $exonStart + 1;
                $startPosiInExon = 1 if ( $startPosiInExon < 1 );
                $endPosiInExon = $absEnd - $exonStart + 1;
                $endPosiInExon = $exonLength if ( $endPosiInExon > $exonLength );
            }
            elsif ( $strand eq "-" ) {
                $startPosiInExon = $exonEnd - $absEnd + 1;
                $startPosiInExon = 1 if ( $startPosiInExon < 1 );
                $endPosiInExon = $exonEnd - $absStart + 1;
                $endPosiInExon = $exonLength if ( $endPosiInExon > $exonLength );
            }

            my $relStart += $relExonStart + $startPosiInExon;
            my $relEnd += $relExonStart + $endPosiInExon;
	    
	    print "absSatart:$absStart\nexonStart:$exonStart\n";
            $absStartInExon = ( $absStart >= $exonStart ) ? $absStart : $exonStart; 
            $absEndInExon = ( $absEnd >= $exonEnd ) ? $exonEnd : $absEnd; 

            my $overlapString = join ( "\t", $absStartInExon, $absEndInExon, $transID, $relStart, $relEnd );
            push @{$ref_overlapRegion}, $overlapString;
            $overlapCount++;
        }

        $relExonStart += $exonLength;
    }

    return $overlapCount;
}

sub printPosition
{
    my $ref_positions = shift;
    my $outFile = shift;
    my %parameters = @_;

    open ( OUT, ">$outFile" ) or die "Cannot open $outFile to write!\n";
    print STDERR "Output overlapped transcripts to $outFile.\n\t", `date`;
    for ( my $idx = 0; $idx < scalar ( @{$ref_positions} ); $idx++ ) {
        if ( $ref_positions->[$idx]{overlap} ) {
            foreach my $overlap ( @{$ref_positions->[$idx]{overlap}} ) 
#	        {print "======================sl==============$ref_positions->[$idx]{info}";}
                { print OUT join ( "\t", $ref_positions->[$idx]{info}, $overlap), "\n"; }
            
        }
        elsif ( $parameters{printNonOverlap} ) 
            { print OUT join ( "\t", $ref_positions->[$idx]{info}, ".", ".", ".", ".", "."), "\n"; }
    }

    1;
}
