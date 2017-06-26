#!/usr/local/Cellar/gnuplot/5.0.0/bin/gnuplot -persist
#
#    
#    	G N U P L O T
#    	Version 5.0 patchlevel 0    last modified 2015-01-01 
#    
#    	Copyright (C) 1986-1993, 1998, 2004, 2007-2015
#    	Thomas Williams, Colin Kelley and many others
#    
#    	gnuplot home:     http://www.gnuplot.info
#    	faq, bugs, etc:   type "help FAQ"
#    	immediate help:   type "help"  (plot window: hit 'h')
# set terminal x11 
# set output
set terminal png
set output 'quiz_count.png'
set key bottom left reverse inside Left
set yrange [1:*]
set logscale y 10
set title "Quiz Questions Answered By Week Since Inception"
set ylabel "Quantity"
#set xdata time
#set timefmt "%s"
#plot 'quiz.txt' using 2:1 smooth csplines with linespoints t "Accuracy"
set style data points
#nz(x) = (x > 100) ? 100 : x 
nz(x) = x
plot 'quiz_count.txt' using 1:(nz($3)) t "Vocab", '' using 1:(nz($4)) t "Pics", '' using 1:5 t "Aud", '' using 1:6 t "POS", '' using 1:7 t "Triv", '' using 1:8 t "Pnouns", '' using 1:9 t "Provs", '' using 1:10 t "Syns", '' using 1:11 t "Living", '' using 1:12 t "Reng", '' using 1:13 t 'TOT'
