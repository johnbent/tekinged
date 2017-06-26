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
set output 'quiz.png'
set key bottom left
set yrange [0:1]
set title "Quiz Accuracy By Week Since Inception"
set ylabel "Accuracy"
#set xdata time
#set timefmt "%s"
#plot 'quiz.txt' using 2:1 smooth csplines with linespoints t "Accuracy"
set style data points
f(x) = m*x + b
g(x) = n*x + c
h(x) = o*x + d
i(x) = p*x + e
j(x) = q*x + f
k(x) = r*x + g
m(x) = s*x + h
n(x) = v*x + i
fit f(x) 'quiz.txt' using 1:3 via m,b
fit g(x) 'quiz.txt' using 1:4 via n,c
fit h(x) 'quiz.txt' using 1:5 via o,d
fit i(x) 'quiz.txt' using 1:6 via p,e
fit j(x) 'quiz.txt' using 1:7 via q,f
fit k(x) 'quiz.txt' using 1:8 via r,g
fit m(x) 'quiz.txt' using 1:9 via s,h
fit n(x) 'quiz.txt' using 1:10 via v,i
#fit o(x) 'quiz.txt' using 1:11 via aa,bb
#fit p(x) 'quiz.txt' using 1:12 via aa,bb
plot 'quiz.txt' \
        using 1:3 t "Classic" lc 1, \
     '' using 1:4 t "Pictures" lc 2, \
     '' using 1:5 t "Audio" lc 3, \
     '' using 1:6 t "Parts of Speech" lc 4, \
     '' using 1:7 t "Trivia" lc 5, \
     '' using 1:8 t "Pronouns" lc 6, \
     '' using 1:9 t "Proverbs" lc 7, \
     '' using 1:10 t "Synonyms" lc 8, \
     '' using 1:11 t "Living Things" lc 9, \
     '' using 1:12 t "Reng Expressions" lc 10, \
     f(x) not lc 1, \
     g(x) not lc 2, \
     h(x) not lc 3, \
     i(x) not lc 4, \
     j(x) not lc 5, \
     k(x) not lc 6, \
     m(x) not lc 7, \
     n(x) not lc 8
     #o(x) not lc 9, \
     #p(x) not lc 10
