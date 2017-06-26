#! /usr/bin/env python

import sys
import pymysql
import string
import re
import os
import belau

def query(q,c):
  c.execute(q)
  return c.fetchall()

def print_footer():
  print '</d:dictionary>'

def print_header():
  print '''<?xml version="1.0" encoding="UTF-8"?>
<!--
  This is a sample dictionary source file.
  It can be built using Dictionary Development Kit.
-->
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng"> '''

def add_image(wid,pal):
  if os.path.isfile('OtherResources/Images/%d.jpg' % wid ):
    print '''\
          <span class="picture">
          <img src="Images/%d.jpg" alt="%s"/>
          </span>''' % ( wid, pal )
    
def space(multiplier=1):
  width=5*multiplier
  return '<span style="display:inline-block; width: %dpx;"></span>' % width

def add_branch_words(branches):
  #print row
  for row in branches: 
    display_word(row,'b')

def display_word(row,htype):
  def print_english(eng):
    if eng:
      return eng
    else:
      return ''

  print '\t<div d:priority="2" class="entry">%s<%s style="display: inline">%s</%s> %s <i>%s</i> %s %s' % ( space(), htype, row['pal'], htype, space(), row['pos'], space(), print_english(row['eng']) )
  if row['pdef']:
    print '\t<span class="pdef" d:priority="2">%s</span>' % row['pdef']
  print '</div>'

def get_pal(wid,c):
  q='select pal from all_words3 where id=%d' % wid
  pal = query(q,c)[0]['pal']
  return pal

def get_regexes(word,branches):
  regex=''
  branches = branches + (word,)
  for branch in branches:
    regex+="lower(palauan) regexp '[[:<:]]%s[[:>:]]' or " % branch['pal']
  regex+='0'
  return regex 

def add_proverbs(word,branches,c):
  add_sentences(word,branches,c,'proverbs','PROVERBS','english','explanation')

def add_examples(word,branches,c):
  add_sentences(word,branches,c,'examples','JOSEPHS DICTIONARY EXAMPLE SENTENCES','english')

def add_uploads(word,branches,c):
  add_sentences(word,branches,c,'upload_sentence','VOLUNTEER UPLOADED EXAMPLE SENTENCES','eng')

def add_sentences(word,branches,c,table,label,english,explanation=None):
  q='select * from %s where %s limit 5' % (table, get_regexes(word,branches))
  examples = query(q,c)
  if examples:
    print '<span class="column">'
    print label 
    for example in examples:
      if explanation:
        explanation_text = '[%s]' % example[explanation]
      else:
        explanation_text = ''
      print '<div class="entry"><i>%s</i> %s %s</div>' % ( example['palauan'], example[english], explanation_text )
    print '</span>'
  #print branches

def add_synonyms(row,c):
  q='select word as b from synonyms where grouping in (select grouping from synonyms where word=%d) and word !=%d' % (row['id'],row['id'])
  add_extras(q,c,'SYNONYMS')

def add_links(row,c):
  q='select b from cf where a=%d union all select a from cf where b=%d' % (row['id'],row['id'])
  add_extras(q,c,'SEE ALSO')

def add_extras(q,c,label):
  extras = query(q,c)
  if extras:
    print '<div class="extra" d:priority="2"><h1 style="display: inline">%s:</h1>' % label
    for extra in extras:
      print get_pal(extra['b'],c)
    print '</div>'

def print_word(row,c):
  # get the branch words
  branches = query('select id,pal,eng,pdef,pos from all_words3 where stem=%d and stem!=id order by pal' % row['id'], c)

  # main header for each word
  print '<d:entry id="%s_%d" d:title="%s">' % ( row['pal'], row['id'], row['pal'] )

  # index entries for the word and its branches
  print '\t<d:index d:value="%s"/>' % row['pal']
  for branch in branches:
    print '\t<d:index d:value="%s"/>' % branch['pal']

  # show a header 
  print '<div d:priority="2"><h1>%s</h1></div>' % row['pal']

  # now show the word
  display_word(row,'b')

  # now add the branches
  add_branch_words(branches)

  # now add extras 
  add_links(row,c)
  add_synonyms(row,c)
  add_examples(row,branches,c)
  add_uploads(row,branches,c)
  add_proverbs(row,branches,c)

  # now add the picture
  add_image(row['id'],row['pal'])

  # end the word
  print '</d:entry>'


def main():
  (db,c) = belau.connect()

  print_header()

  q = "select id,pal,eng,pdef,pos,oword,origin from all_words3 where id=stem and pal in ('rubak', 'meas', 'mengelebed', 'chelebed','omar')";
  for row in query(q,c):
    print_word(row,c)

  print_footer()

  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()


