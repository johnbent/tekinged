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
qc1.append_field('Title','The Text from the Column')
 
fta1 = FreeTextAnswer(num_lines=40) 
 
q1 = Question(identifier='first',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
 
#--------------- CREATE THE HITS -------------------

description="""Copy all the text from one column of the dictionary. Transcribe accented
characters as if they do not have an accent. If there is a guide word at the
top, do not transcribe it.  If there is a page number at the bottom, do not
transcribe it.  If there is partial text for a second column that wasn't
cropped completely off, do not
transcribe it. Transcribe long dashes within lines as a double dash ('--').
For all lines belonging to one word entry, do not hit enter.  Just write the
entire entry as one line.  Do hit enter between entries.
If there is a hyphen and the next line is available, then do not transcribe
the hypen; just merge the two lines.  If there is a phonetic pronounciation
listed in brackets (e.g. [kudg]) then do not transcribe it.  If there is a hypen on the last
line of the column, then transcribe it as a single dash ('-')"""


# 60 to 407
for i in range(60,61):
  for side in ( 'left', 'right' ):
    title = 'Transcribe Palauan Dictionary Page %d Column %s' % (i , side)
    #---------------  BUILD OVERVIEW -------------------
     
    overview = Overview()
    overview.append_field('Title', title)
    overview.append(FormattedContent(description))
    url="http://tekinged.com/png-halves/dict-%03d-%s.png" % (i,side)
    content="<a href='%s'><img alt='IMAGE TO TRANSCRIBE' src='%s' width='50%%' /></a>" % (url,url)
    print "Entering hit for %s" % url
    overview.append(FormattedContent("Use these links to see an example image and how it should be transcribed"))
    overview.append(FormattedContent('<a target="_blank"'
                                     ' href="http://tekinged.com/misc/mturk/image.png">'
                                     ' Example Image</a>'))
    overview.append(FormattedContent('<a target="_blank"'
                                     ' href="http://tekinged.com/misc/mturk/text.png">'
                                     ' Example Transcription</a>'))
    overview.append(FormattedContent("Here is the image to be transcribed:"))
    overview.append(FormattedContent(content))
   
     
    #--------------- BUILD THE QUESTION FORM -------------------
   
    question_form = QuestionForm()
    question_form.append(overview)
    question_form.append(q1)
   
    mtc.create_hit(questions=question_form,
                 qualifications=quals,
                 max_assignments=1,
                 title=title,
                 description=description,
                 keywords=keywords,
                 duration = 60*30,
                 reward=0.30)
