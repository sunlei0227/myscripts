#! /Share/home/zhangqf/usr/perl-5.22.1/bin/perl 
use warnings;  
#use strict;  
use threads;  
use Thread::Semaphore;  
use File::Basename qw(basename);  
  
die "perl $0 <bam> \n" if @ARGV != 1;  
  
#my $semaphore = Thread::Semaphore->new($ARGV[1]);  
my $id = basename($ARGV[0], ".bam");  
if(-s "$ARGV[0].bai")  
{  
      
}else{  
    `samtools index $ARGV[0]`;  
}  
my $outdir = "${id}_split";  
mkdir $outdir;  
  
my (%hash, $hd, $rg, $pg);  
open HEAD, "samtools view -H $ARGV[0] |" or die $!;  
while(<HEAD>)  
{  
    if(/^\@SQ/)  
    {  
        my ($chr) = $_ =~ /SN:(\S+)/;  
        $hash{$chr} = $_;  
        next;  
    }  
    if(/^\@HD/)  
    {  
        $hd .= "$_";  
        next;  
    }  
    if(/^\@RG/)  
    {  
        $rg .= "$_";  
        next;  
    }  
    if(/^\@PG/)  
    {  
        $pg .= "$_";  
        next;  
    }  
}  
  
foreach(keys %hash)  
{  
#    $semaphore->down();  

	&splitchr($_);
#    my $thread = threads->create(\&splitchr, $_);  
    print ".\n";
#    $thread->detach();  

}  
=cutss
&waitDone;  
  
sub waitDone{  
    my $num = 0;  
    while($num < $ARGV[1])  
    {  
        $semaphore->down();  
        $num ++;  
    }  
}  
=cut 
sub splitchr{  
    my $chr = shift;  
    open $chr, "> $outdir/$id.$chr.sam" or die $!;  
#    print $chr "$hd$hash{$chr}$rg$pg";  
    print $chr "$hd$hash{$chr}"; 
    my $content = `samtools view $ARGV[0] $chr`;  
    print $chr "$content";  
    close $chr;  
    `samtools view -bS $outdir/$id.$chr.sam > $outdir/$id.$chr.bam`;  
    #`rm $outdir/$id.$chr.sam -rf`;  
}  
