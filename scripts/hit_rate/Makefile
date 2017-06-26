MYS=$(shell grep mysql $(HOME)/.bashrc)
MYS=$(shell egrep '^\s+mysql' $(HOME)/.bashrc)

all: set_tunnel hits.png quiz.png quiz_count.png visitors.png quiz_avg.png quiz_count.png quiz_popularity.png
	open *.png

set_tunnel:
	bash -i -c tunnel	# this is a bash function from my bashrc.  Can we call it from here?

visitors.txt:
	# the sed removes the last line which is an inaccurate line because it shows up as visitors per week but the last week is probably not 7 days long yet 
	./get_visitors.py | sed '$$d' > $@ 

visitors.png: visitors.txt
	gnuplot -e "filename='$^'" visitors.gnu > $@

quiz_avg.png: quiz_avg.txt
	gnuplot -e "set ylabel 'Average (%s)'; set title 'Average Score by Quiz Type'" quiz_avg.gnu < $^ > $@

quiz_popularity.png: quiz_popularity.txt
	gnuplot -e "set ylabel 'Popularity (%s)'; set title 'Popularity by Quiz Type'" quiz_avg.gnu < $^ > $@

quiz.png: quiz.txt
	gnuplot quiz.gnu
	gnuplot quiz_smooth.gnu

quiz_count.png: quiz_count.txt
	gnuplot quiz_count.gnu

hits.png: hits.txt
	gnuplot hits.gnu 

QUIZ_SED=sed 's/Parts of Speech/POS/' | sed 's/Living Things/Living/' | sed 's/Reng Expression/Reng/' 

quiz_avg.txt:
	echo "select quiztype,avg(correct*4) as Percent,std(correct) as Deviation from log_quizzes group by quiztype;" | $(MYS) -N | $(QUIZ_SED) > $@

quiz_popularity.txt:
	echo "select '#',@total:=count(*) from log_quizzes; select quiztype,100*count(*)/@total,'0' from log_quizzes group by quiztype;" | $(MYS) -N | $(QUIZ_SED) > $@

quiz_count.txt:
	python quiz_scores.py c | tee $@

quiz.txt:
	python quiz_scores.py | tee $@

hits.txt:
	python get_hit_rate.py | tee $@

clean:
	\rm -f *.txt *.png
