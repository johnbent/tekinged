#! /usr/bin/env python

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
ACCESS_ID ="AKIAIRZ5JZ2KFCLKU4MQ"
SECRET_KEY = "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"
HOST = 'mechanicalturk.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = 'Transcribe a Palauan proverb'
description = ('Copy a proverb from an online PDF and paste'
               ' it into the provied fields')
keywords = 'website, rating, opinions'
 
#---------------  BUILD QUESTION 1 -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','The Palauan Language Proverb')
 
fta1 = FreeTextAnswer() 
 
q1 = Question(identifier='palauan',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
 
#---------------  BUILD QUESTION 2 -------------------
 
qc2 = QuestionContent()
qc2.append_field('Title','The English Language Translation')
 
fta2 = FreeTextAnswer()
 
q2 = Question(identifier="english",
              content=qc2,
              answer_spec=AnswerSpecification(fta2))
 
#---------------  BUILD QUESTION 3 -------------------
 
qc3 = QuestionContent()
qc3.append_field('Title','The Longer Explanation (if any)')
 
fta3 = FreeTextAnswer()
 
q3 = Question(identifier="english",
              content=qc3,
              answer_spec=AnswerSpecification(fta3))
 
#--------------- CREATE THE HITS -------------------

for i in range(5,245):
  print "Entering hit for Proverb %d" % i
  title = 'Transcribe Palauan Proverb Number %d' % i 
  description='Copy Proverb %d from the PDF and enter it into the fields' % i
 
  #---------------  BUILD OVERVIEW -------------------
   
  overview = Overview()
  overview.append_field('Title', title)
  overview.append(FormattedContent(description))
  overview.append(FormattedContent('<a target="_blank"'
                                   ' href="http://pages.cs.wisc.edu/~johnbent/belau/misc/proverbs.pdf">'
                                   ' Palauan Proverbs</a>'))
   
  #--------------- BUILD THE QUESTION FORM -------------------
 
  question_form = QuestionForm()
  question_form.append(overview)
  question_form.append(q1)
  question_form.append(q2)
  question_form.append(q3)
 
  mtc.create_hit(questions=question_form,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.03)
