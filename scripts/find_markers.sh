#! /bin/bash

for i in {41..518}
do
  p=`printf %03d $i`
  image="page-$p.png"
  open $image
  echo "What is marker?"
  read marker
  command="insert into kerresel_pages (last) values ('$marker')"
  echo $command | mysql --password=$TEK_PWD -u $TEK_USR -h mysql.tekinged.com -D belau
  echo $command | tee -a commands.mysql 
done
