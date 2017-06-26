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
set terminal png
set style fill   solid 0.30 border
set grid ytics
unset key
set style histogram errorbars gap 2 lw 1title textcolor lt -1
set style data histograms
#set title "Accuracy by Quiz Type" 
set xrange [*:*] 
#set ylabel "Accuracy (%)" 
set xtics rotate out
set yrange [0:100] noreverse nowriteback
plot '<cat' using 2:3:xticlabels(1) title columnheader
