#! /usr/bin/env bash

. $HOME/.bashrc

date="2015-06-13"

d="trussel.$date"
mkdir -p $d 
for i in all_words3 cf examples pictures pos proverbs upload_audio upload_sentence
do
  echo $i
  touch $d/$i
  q="select * from $i where added > '$date'\G;"
  echo "$q"
  echo "$q" | mys > $d/$i
done
