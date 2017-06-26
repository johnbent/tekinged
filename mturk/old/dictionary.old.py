#! /usr/bin/env python

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from boto.mturk.qualification import LocaleRequirement,PercentAssignmentsApprovedRequirement,Qualifications,NumberHitsApprovedRequirement
 
ACCESS_ID ="AKIAIRZ5JZ2KFCLKU4MQ"
SECRET_KEY = "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"
#HOST = 'mechanicalturk.amazonaws.com'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = 'Transcribe Palauan Dictionary entries' 
description = ('Transcribe a column from Palauan-English dictionary' )
keywords = 'transcribe, data entry, google form, dictionary, palauan language'

#---------------  QUALIFICATIONS -------------------
quals = Qualifications()
quals.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan",integer_value=98))
quals.add(NumberHitsApprovedRequirement("GreaterThan",1000))

 
#---------------  BUILD QUESTION 1 -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','The first word transcribed')
 
fta1 = FreeTextAnswer() 
 
q1 = Question(identifier='first',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
 
#---------------  BUILD QUESTION 2 -------------------
 
qc2 = QuestionContent()
qc2.append_field('Title','The last word transcribed')
 
fta2 = FreeTextAnswer()
 
q2 = Question(identifier='last',
              content=qc2,
              answer_spec=AnswerSpecification(fta2))
 
#---------------  BUILD QUESTION 3 -------------------
 
qc3 = QuestionContent()
qc3.append_field('Title','The dictionary page number')
 
fta3 = FreeTextAnswer()
 
q3 = Question(identifier='pageno',
              content=qc3,
              answer_spec=AnswerSpecification(fta3))
 
#--------------- CREATE THE HITS -------------------

#3 to 350
for i in range(10,12):
  print "Entering hit for Page %d" % i
  title = 'Transcribe Palauan Dictionary Page Number %d' % i 
  description='Copy the entries from page %d (as shown at the bottom of the page) from the PDF and enter them as google forms' % i
  description2='If a word starts on a previous page and ends on your page, do not transcribe.  If a word starts on your page and ends on the next page, then do transcribe.'
 
  #---------------  BUILD OVERVIEW -------------------
   
  overview = Overview()
  overview.append_field('Title', title)
  overview.append(FormattedContent(description))
  overview.append(FormattedContent(description2))
  overview.append(FormattedContent('<a target="_blank"'
                                   ' href="http://tekinged.com/misc/eleanor/dictionary.pdf">'
                                   ' Palauan Dictionary</a>'))
  overview.append(FormattedContent('<a target="_blank"'
                                   ' href="http://goo.gl/forms/Q3omxHF5PH">'
                                   ' Google Form</a>'))
  overview.append(FormattedContent('<a target="_blank"'
                                   ' href="http://tekinged.com/misc/mturk/example1.png">'
                                   ' Example One</a>'))
  overview.append(FormattedContent('<a target="_blank"'
                                   ' href="http://tekinged.com/misc/mturk/example2.png">'
                                   ' Example Two</a>'))
   
  #--------------- BUILD THE QUESTION FORM -------------------
 
  question_form = QuestionForm()
  question_form.append(overview)
  question_form.append(q1)
  question_form.append(q2)
  question_form.append(q3)
 
  mtc.create_hit(questions=question_form,
               qualifications=quals,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*30,
               reward=1.00)
