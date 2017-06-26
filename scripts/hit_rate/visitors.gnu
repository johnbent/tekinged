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
set key top left
set title "Visitors per Week"
set ylabel "Visitors"
#set ytics 250
set grid ytics
set style data linespoints
#set yrange [1:10000]
set logscale y 2
set logscale y2 2
set ytics border mirror norotate autofreq
set y2tics
plot filename using 1:2 t "Visitors" , '' using 1:3 t "Searchers" , '' using 1:4 t "Quizzers" 
#plot filename using 1:2 t "Visitors" at end, '' using 1:3 t "Searchers" at end, '' using 1:4 t "Quizzers" at end
