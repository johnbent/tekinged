#!/usr/local/Cellar/gnuplot/5.0.0/bin/gnuplot -persist

set terminal png font "/Library/Fonts/Arial.ttf" 14
set output 'freq.png'

set title "Palauan Language Word Usage Frequency"

# labels
unset label
set label 1000 "[Only a few \nselected words shown.]" at graph 0.6,0.9
set label 1 "A"  at 1.10, 23.0, 0.00000 left 
set label 2 "EL" at 2.00, 11.0, 0.00000 center 
set label 3 "ER" at 3.00,  8.0, 0.00000 center 
set label 4 "E"  at 3.00,  2.2 left
set label 5 "NGII" at 4.8, 3.0 left
set label 7 "NG" at 7, 1.563 left
set label 10 "DIAK" at 10, 0.8 left
set label 12 "CHAD" at 10.8, 0.6 right
set label 18 "UNGIL" at 16, 0.396 right 
set label 20 "RENGUL" at 23, 0.335 left
set label 26 "NGIKEL" at 23, 0.252 right
set label 45 "UDOUD" at 46, 0.159 right
set label 49 "DAOB" at 49, 0.143 left
set label 100 "LMUUT" at 80, 0.073 right
set label 128 "MESISIICH" at 160, 0.056 left
set label 165 "SECHAL" at 165, 0.044 right
set label 207 "REDIL" at 220, 0.034 left
set label 384 "NGEASEK" at 344, 0.017 right
set label 567 "CHEBUUL" at 587, 0.011 left
set label 665 "ORRECHED" at 610, 0.009 right
set label 999 "BLSOIL" at 970, 0.006 right
set label 1484 "CHELISEKSIKD" at 1400, 0.0035 right
set label 3383 "TOKLECHAD" at 3300, 0.002 right
#set label 2374 "MEREKII" at 2300,0.003 right
#set label 1187 "CHIROCHER" at 1100, 0.005 right

set xrange [ 0.900000 : * ] noreverse nowriteback
set xlabel "Rank"
set yrange [ * : 100 ]
set ylabel "Frequency of Usage (%)" 

set logscale x 10
set logscale y 10

plot 'data' using 6:4 not
