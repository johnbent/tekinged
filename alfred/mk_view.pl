print "CREATE VIEW organized AS ";
while(<>) {
  chomp;
  ($table,$col) = split('\.',$_);
  print "SELECT $col as Palauan from $table where length($col)>0 UNION\n";
}
