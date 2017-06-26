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
set output 'quiz_smooth.png'
set key bottom left
set yrange [0:1]
set title "Quiz Accuracy By Week Since Inception"
set ylabel "Accuracy"
#set xdata time
#set timefmt "%s"
#plot 'quiz.txt' using 2:1 smooth csplines with linespoints t "Accuracy"
set style data points
plot 'quiz.txt' using 1:3 t "Classic Smooth" smooth bezier, \
     '' using 1:4 t "Pics Smooth" smooth bezier, \
     '' using 1:5 t "Audio Smooth" smooth bezier, \
     '' using 1:6 t "POS Smooth" smooth bezier, \
     '' using 1:7 t "Trivia Smooth" smooth bezier, \
     '' using 1:8 t "Pronouns Smooth" smooth bezier, \
     '' using 1:9 t "Proverbs Smooth" smooth bezier, \
     '' using 1:10 t "Syn Smooth" smooth bezier, \
     '' using 1:10 t "Living Smooth" smooth bezier, \
     '' using 1:10 t "Reng Smooth" smooth bezier
