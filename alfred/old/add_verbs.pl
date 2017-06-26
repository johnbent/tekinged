#! /bin/env perl

use strict;

while(<>) {
  chomp;
  my ($imperfect, $p3s, $p3p, $pp3s, $pp3p, $state, $antic) = split;
  my $perf_3pp = 'perf_3pp_inan';
  my $past_perf_3pp = 'past_perf_3pp_inan';
  if ($p3p =~ m/terir$/) {
    warn "$p3p is human suffix pronoun\n";
    $perf_3pp = 'perf_3pp';
    $past_perf_3pp = 'past_perf_3pp';
  }
  my $update = "update verbs set ";
  $update .= "perf_3ps='$p3s'";
  $update .= ",$perf_3pp='$p3p'" unless $p3p eq '--';
  $update .= ",past_perf_3ps='$pp3s'" unless $pp3s eq '--';
  $update .= ",$past_perf_3pp='$pp3p'" unless $pp3p eq '--';
  $update .= ",resulting_state='$state'" if $state; 
  $update .= ",anticipating='$antic'" if $antic;
  my $where = "where imperfect like '$imperfect';";
  print "select '$imperfect'; $update $where\n";
}
