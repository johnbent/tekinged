#! /usr/bin/bash

while read p
do
    grep -q -l "$p" *
    if [ $? -eq 0 ]
    then
      echo "update all_words3 set josephs=1 where trim(pal) like '$p';"
    fi
done
