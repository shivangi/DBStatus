package FormID;

use strict;
use warnings;

require Exporter;
use DBI;

our @ISA = qw(Exporter);

our %EXPORT_TAGS = ( 'all' => [ qw(
        get
        save
) ] );

our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );

our @EXPORT = qw(

);

our $version = '0.1';
our $FILE = 'formid';

sub save {
    my $fid = shift;

    open(FORMID, ">${FILE}") or die("Cannot open $FILE: $!");
    print FORMID $fid, "\n";
    close(FORMID);
}

sub get {
    open(FORMID, "${FILE}") or die("Cannot open $FILE: $!");
    my $fid = <FORMID>;
    chomp($fid);
    close(FORMID);

    return int($fid);
}
