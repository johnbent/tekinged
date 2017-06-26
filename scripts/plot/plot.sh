#! /bin/bash

shopt -s expand_aliases
source ~/.bashrc
rm -f /tmp/out
echo 'tee /tmp/out; select id,unix_timestamp(added) from all_words3 where !isnull(added) order by id;' | mys --skip-column-names
echo "set terminal png; set output 'plot.png'; set xdata time; set timefmt '%s'; set format x '%s'; plot '/tmp/out' using 2:1" | gnuplot
