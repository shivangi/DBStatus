package Utility::FormXMLParser;
use base qw(XML::SAX::Base);
use strict;
use vars qw($query);

# Overridden methods

sub start_document {
}

sub end_document {
}

sub start_element {
    my $self = shift;
    my $el = shift;

    my $lname = $el->{LocalName};

    if ($lname eq 'query') {
    }

}

sub end_element {
    my $self = shift;
    my $el = shift;

    my $text = $self->get_text;

    my $lname = $el->{LocalName};
    if ($lname eq 'query') {
        $query= $text;
    }
}

sub get_text {
    my $self = shift;
    my $text = '';

    if (defined($self->{text})) {
        $text = $self->{text};
        $self->{text} = '';
    }
    return $text;
}

sub characters {
    my $self = shift;
    my $text = shift;

    $self->{text} .= $text->{Data};
}

sub query{
  return $query;
}

1;
